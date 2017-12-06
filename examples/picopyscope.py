#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 *     Filename: picopyscope.py
 *     
 *	   Description:
 *			Example Python application with GUI
 *			demonstrating how to capture data from 
 *			PicoScope oscilloscopes.
 * 	   
 *    Created on 18 Nov 2014
 *
 *	  @author: mario
 *
 *    Copyright (C) 2014 - 2017 Pico Technology Ltd. See LICENSE file for terms.
 *
"""

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.dockarea.Dock import Dock
import pyqtgraph.ptime as ptime
import importlib
import sys
import threading as th
import numpy as np
from picosdk import picostatus as ps, psutils


class PicoPyDriver(object):
    def __init__(self, name):
        self.name = name
        self.available = False
        self.module = None
        self.serials = []
        try:
            self.module = importlib.import_module("picosdk.%s" % name)
            self.available = True
        except Exception as ex:
            print "module:", ex.message


class PicoPyChannel(object):
    chanstr = "ABCDEFGHIJKLMNOPQRSTUVXYZ"
    pens = {0: pg.mkPen(0, 0, 255),
            1: pg.mkPen(255, 0, 0),
            2: pg.mkPen(0, 255, 0),
            3: pg.mkPen(255, 255, 0),
            4: pg.mkPen(170, 0, 255),
            5: pg.mkPen(210, 210, 210),
            6: pg.mkPen(170, 255, 255),
            7: pg.mkPen(255, 85, 127)}

    def __init__(self, number):
        self.number = number
        self.letter = self.chanstr[self.number]
        self.longName = "Channel %s" % self.letter
        self.shortName = "Ch %s" % self.letter
        self.dock = Dock(self.longName, area=None, size=(100, 50), widget=None, hideTitle=False, autoOrientation=False)
        self.dock.setFixedHeight(50)
        self.widget = pg.LayoutWidget()
        self.dock.addWidget(self.widget, row=0, col=0, rowspan=1, colspan=1)
        self.enabled = QtGui.QCheckBox("")
        self.enabled.stateChanged.connect(self._enabledChange)
        self.widget.addWidget(self.enabled, row=0, col=0, rowspan=0, colspan=1)
        self.pen = self.pens[self.number]
        self.picker = pg.ColorButton(color=self.pen.color())
        self.picker.sigColorChanging.connect(self.pickChange)
        self.picker.sigColorChanged.connect(self.pickDone)
        self.picker.setFixedSize(28, 21)
        self.picker.setFlat(True)
        self.widget.addWidget(self.picker, row=0, col=2, rowspan=0, colspan=1)
        self.ranges = QtGui.QComboBox()
        self.ranges.currentIndexChanged.connect(self._rangesChange)
        self.widget.addWidget(self.ranges, row=0, col=3, rowspan=0, colspan=500)
        self.plot = None
        self.xdata = None
        self.ydata = None
        self.enum = None
        self.range = None
        self.rangeMap = {}
        self.resetRange = False

        self.lock = th.Lock()
        if self.lock.acquire(False):
            self.lock.release()

        self.freeze(True)
        self.ranges.setEnabled(False)

    def _enabledChange(self, state):
        self.ranges.setEnabled(state)

    def _rangesChange(self, index):
        if index in self.rangeMap:
            if self.rangeMap[index] is not None:
                self.range = self.rangeMap[index].enum
            else:
                self.range = None
        last = self.ranges.count() - 1
        if index == last:
            self.resetRange = True
        else:
            self.ranges.setItemText(last, "AutoMax")

    def setEnabled(self, state):
        self.enabled.setChecked(state)
        self._enabledChange(state)

    def isEnabled(self):
        return self.enabled.isChecked()

    def freeze(self, state):
        self.widget.setEnabled(not state)

    def loadRanges(self, ranges):
        state = self.ranges.isEnabled()
        if state:
            self.ranges.setEnabled(False)
        self.ranges.clear()
        index = 0
        for r in ranges.keys():
            self.ranges.addItem(ranges[r].label, userData=QtCore.QVariant(r))
            self.rangeMap[index] = ranges[r]
            index += 1
        self.ranges.addItem("AutoMax", {'userData': None})
        self.ranges.setCurrentIndex(index)
        self.rangeMap[index] = None
        self.range = None
        if state:
            self.ranges.setEnabled(True)

    def draw(self):
        if self.lock.acquire(False):
            try:
                if self.plot is not None and self.ydata is not None:
                    if self.xdata is None:
                        self.plot.setData(self.ydata)
                    else:
                        self.plot.setData(x=self.xdata, y=self.ydata)
                    self.plot.update()
            except Exception as ex:
                print "channel %d draw:" % self.number, ex.message
            finally:
                self.lock.release()

    def pickChange(self, button):
        pass

    def pickDone(self, button):
        self.pen.setColor(button.color())


class PicoPyDeviceWorker(QtCore.QObject):
    finished = QtCore.SIGNAL("finished")
    freezeUI = QtCore.SIGNAL("freezeUI")
    freezeDeviceKnob = QtCore.SIGNAL("freezeDeviceKnob")
    startStopReset = QtCore.SIGNAL("startStopReset")
    popChannels = QtCore.SIGNAL("popChannels")
    plotChannels = QtCore.SIGNAL("plotChannels")
    updateYrange = QtCore.SIGNAL("updateYrange")
    updateInterval = QtCore.SIGNAL("updateInterval")
    updateStats = QtCore.SIGNAL("updateStats")

    def __init__(self, picops):
        QtCore.QObject.__init__(self)
        self.picops = picops

    def _purgeUnits(self):
        current = self.picops.deviceKnobSelect.itemText(self.picops.deviceKnobSelect.currentIndex())
        while self.picops.deviceKnobSelect.count() > 2:
            i = 1
            while current == str(
                    self.picops.deviceKnobSelect.itemText(i)) and i < self.picops.deviceKnobSelect.count():
                i += 1
            self.picops.deviceKnobSelect.removeItem(i)
        for driver in self.picops.drivers.keys():
            self.picops.drivers[driver].serials = []

    def enumerator(self):
        firstRun = True
        while firstRun or not self.picops.eventExit.wait(5):
            firstRun = False
            # print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if self.picops.deviceKnobSelect.currentIndex() == 0 and self.picops.driverAccessLock.acquire(False):
                try:
                    for driver in self.picops.drivers.keys():
                        serials = self.picops.drivers[driver].module.enumerate_units()
                        if self.picops.eventExit.is_set():
                            break
                        if len(serials) > 0:
                            for serial in serials:
                                if len(serial) > 0:
                                    print "found %s: %s" % (driver, serial)
                                    if serial not in self.picops.drivers[driver].serials:
                                        self.picops.deviceKnobSelect.addItem(
                                            "%s %s" % (driver.upper(), serial), userData=None)
                                        self.picops.drivers[driver].serials += [serial]
                        for serial in self.picops.drivers[driver].serials:
                            if serial not in serials:
                                index = self.picops.deviceKnobSelect.findText("%s %s" % (driver.upper(), serial))
                                if index > 0 and index != self.picops.deviceKnobSelect.currentIndex():
                                    self.picops.deviceKnobSelect.removeItem(index)
                                    self.picops.drivers[driver].serials.remove(serial)
                except Exception as ex:
                    print "enumerator:", ex.message
                finally:
                    self.picops.driverAccessLock.release()
                if self.picops.deviceKnobSelect.count() >= 2:
                    self.emit(self.freezeDeviceKnob, False)
                    if self.picops.deviceKnobSelect.count() == 2:
                        self.picops.deviceKnobSelect.setCurrentIndex(1)
                    else:
                        self.picops.deviceKnobSelect.setItemText(0, "Select device")
        self.emit(self.finished)

    def opener(self):
        # print "opener lock"
        self.picops.driverAccessLock.acquire(True)
        # print "opener locked"
        self.emit(self.freezeUI, True)
        self.emit(self.freezeDeviceKnob, True)
        try:
            if self.picops.currentDevice is not None:
                self.picops.currentDevice.close_unit()
                self.picops.currentDevice = None
            self.picops.deviceKnobSelect.setItemText(0, "Openning...")
            index = self.picops.deviceKnobSelect.currentIndex()
            text = str(self.picops.deviceKnobSelect.itemText(index))
            driver, serial = text.split(" ")
            driver = driver.lower()

            if driver in self.picops.drivers:
                if serial in self.picops.drivers[driver].serials:
                    if self.picops.currentDevice is None:
                        self.picops.currentDevice = self.picops.drivers[driver].module.Device()
                        currDev = self.picops.currentDevice
                        status = currDev.open_unit(serial)
                        if status in (ps.pico_num("PICO_OK"),
                                      ps.pico_num("PICO_USB3_0_DEVICE_NON_USB3_0_PORT"),
                                      ps.pico_num("PICO_POWER_SUPPLY_NOT_CONNECTED")):
                            if status in (ps.pico_num("PICO_USB3_0_DEVICE_NON_USB3_0_PORT"),
                                          ps.pico_num("PICO_POWER_SUPPLY_NOT_CONNECTED")):
                                """ @TODO: confirmation dialogue """
                                status = currDev.set_power_source(ps.pico_num("PICO_POWER_SUPPLY_NOT_CONNECTED"))
                                if status == ps.pico_num("PICO_OK"):
                                    currDev.load_info()
                                else:
                                    print ps.pico_tag(status)
                                    return

                            self._purgeUnits()
                            self.picops.deviceKnobSelect.setItemText(0, "Close Device")
                            self.picops.deviceKnobSelect.setItemText(1, "PS%s %s" % (
                                currDev.info.variant_info, currDev.info.batch_and_serial))
                            print currDev.info
                            status, memps = currDev.set_memory_segments(self.picops.segments)
                            self.picops.samples = min(self.picops.maxSamples, int(memps / currDev.info.num_channels))
                            self.picops.timebaseKnobRatioBin. \
                                setMaximum(int(self.picops.samples / self.picops.minSamples), update=False)
                            self.emit(self.popChannels)

                        else:
                            print ps.pico_tag(status)
                            return
        except Exception as ex:
            print "opener:", ex.message
        finally:
            self.emit(self.freezeUI, False)
            self.emit(self.freezeDeviceKnob, False)
            self.emit(self.startStopReset, False)
            # print "opener unlock"
            self.picops.driverAccessLock.release()
            # print "opener unlocked"
            self.emit(self.finished)

    def closer(self):
        # print "closer lock"
        self.picops.driverAccessLock.acquire(True)
        # print "closer locked"
        try:
            if self.picops.currentDevice is not None:
                self.emit(self.freezeUI, True)
                self.emit(self.freezeDeviceKnob, True)
                self.emit(self.startStopReset)
                self.picops.deviceKnobSelect.setItemText(0, "Wait...")
                self.picops.deviceKnobSelect.removeItem(1)
                self.picops.currentDevice.close_unit()
                self.picops.currentDevice = None
        except Exception as ex:
            print "closer:", ex.message
        finally:
            # print "closer unlock"
            self.picops.driverAccessLock.release()
            # print "closer unlocked"
        self.emit(self.finished)

    def collector(self):
        lastTime = ptime.time()
        while self.picops.eventDataNeeded.wait():
            if self.picops.eventExit.is_set():
                if self.picops.currentDevice is not None:
                    with self.picops.driverAccessLock:
                        self.picops.currentDevice.close_unit()
                break
            if self.picops.currentDevice is None:
                continue
            # print "collector lock"
            self.picops.driverAccessLock.acquire(True)
            # print "collector locked"
            try:
                enabledChannels = 0
                maxRange = -1
                triggChange = False
                """ detect ratio modes changes """
                if self.picops.timebaseRatioReset:
                    index = self.picops.timebaseKnobRatioMode.currentIndex()
                    mode = self.picops.timebaseKnobRatioMode.itemData(index).toInt()[0]
                    ratioMode = PicoPyRatioModes.driverRatioMode(self.picops.currentDevice.m, mode)
                    if ratioMode is not None:
                        self.picops.ratioMode = ratioMode
                        self.picops.ratioBin = int(self.picops.timebaseKnobRatioBin.value())
                        self.picops.timebaseRatioMode = mode
                    self.picops.timebaseRatioReset = False
                    for chan in [c for c in self.picops.channels.keys() if self.picops.channels[c].isEnabled()]:
                        for segment in range(self.picops.segments):
                            index = self.picops.currentDevice.info.num_channels * segment * 2 + chan * 2
                            self.picops.currentDevice.locate_buffer(self.picops.channels[chan].enum,
                                                                    int(self.picops.samples / self.picops.ratioBin),
                                                                    segment, self.picops.ratioMode,
                                                                    self.picops.ratioBin,
                                                                    index)
                """ detect channel state changes """
                for chan in self.picops.channels.keys():
                    stateChanged = False
                    rangeChanged = False
                    status, currState = self.picops.currentDevice.get_channel_state(chan)
                    if currState.enabled and maxRange < currState.range:
                        maxRange = currState.range
                    if status != ps.pico_num("PICO_OK"):
                        continue
                    if currState.enabled != self.picops.channels[chan].isEnabled():
                        stateChanged = True
                        triggChange = True
                        if currState.enabled:
                            """ channel is now disabled """
                            pass
                        else:
                            """ channel become enabled """
                            for segment in range(self.picops.segments):
                                index = self.picops.currentDevice.info.num_channels * segment * 2 + chan * 2
                                self.picops.currentDevice.locate_buffer(self.picops.channels[chan].enum,
                                                                        int(self.picops.samples / self.picops.ratioBin),
                                                                        segment, self.picops.ratioMode,
                                                                        self.picops.ratioBin, index)
                        currState.enabled = self.picops.channels[chan].isEnabled()
                    if self.picops.channels[chan].range is None or currState.range != \
                            self.picops.channels[chan].range:
                        if self.picops.channels[chan].range is None:
                            if currState.overvoltaged \
                                    and currState.range < self.picops.currentDevice.info.max_range:
                                self.picops.currentDevice.increase_channel_range(
                                    self.picops.channels[chan].enum)
                                triggChange = True
                                if maxRange < currState.range + 1:
                                    maxRange = currState.range + 1
                                for nrange in self.picops.channels[chan].rangeMap:
                                    if currState.range + 1 == \
                                            self.picops.channels[chan].rangeMap[nrange].enum:
                                        self.picops.channels[chan].ranges.setItemText(
                                            self.picops.channels[chan].ranges.count() - 1,
                                            "AutoMax (%s)" % self.picops.channels[chan].rangeMap[nrange].label)
                                        break
                            elif (currState.enabled and stateChanged) \
                                    or self.picops.channels[chan].resetRange:
                                currState.range = self.picops.currentDevice.info.min_range
                                rangeChanged = True
                                triggChange = True
                                self.picops.channels[chan].resetRange = False
                        else:
                            currState.range = self.picops.channels[chan].range
                            rangeChanged = True
                            triggChange = True
                            if maxRange < currState.range:
                                maxRange = currState.range
                    if stateChanged or rangeChanged:
                        self.picops.currentDevice.set_channel(self.picops.channels[chan].enum, currState)
                        self.picops.currentDevice.unlock_all_buffers()

                    if currState.enabled:
                        enabledChannels += 1
                if enabledChannels == 0:
                    status = ps.pico_num("PICO_INVALID_CHANNEL")
                else:
                    if self.picops.triggerReset or triggChange:
                        self.picops.triggerReset = False
                        chanEnum = None
                        rangeAbs = None
                        if self.picops.triggerKnobEnabled.isChecked():
                            chanStr = str(self.picops.triggerKnobSource.currentText())
                            for chan in self.picops.channels:
                                if self.picops.channels[chan].shortName == chanStr:
                                    if self.picops.channels[chan].isEnabled():
                                        chanEnum = self.picops.channels[chan].enum
                                        stat, state = self.picops.currentDevice.get_channel_state(chanEnum)
                                        if stat == ps.pico_num("PICO_OK"):
                                            rangeAbs = self.picops.currentDevice.m.Ranges.values[state.range]
                                    break
                        if rangeAbs is not None:
                            triggYthreshold = self.picops.triggY / rangeAbs
                        else:
                            triggYthreshold = 0
                        triggGo = chanEnum is not None and abs(triggYthreshold) <= 1
                        d = 0
                        if triggGo:
                            d, av = self.picops.triggerKnobDirection.itemData(
                                self.picops.triggerKnobDirection.currentIndex()).toInt()
                        if self.picops.triggX is None:
                            self.picops.triggX = 0.5
                        self.picops.currentDevice.set_horizontal_trigger_ratio(self.picops.triggX)
                        self.picops.currentDevice.set_simple_trigger(triggGo,
                                                                     0 if chanEnum is None else chanEnum,
                                                                     triggYthreshold, d, 0,
                                                                     max(1, int(self.picops.interval / 1000000)))

                    status = \
                        self.picops.currentDevice.collect_segment(segment=self.picops.currentSegment,
                                                                  interval=(self.picops.interval / self.picops.samples))
                    if self.picops.maxRange != maxRange:
                        self.picops.maxRange = maxRange
                        self.picops.maxRangeUpdate = True
                if status != ps.pico_num("PICO_OK"):
                    print "collect:", ps.pico_tag(status)
                    if status == ps.pico_num("PICO_BUSY"):
                        status = self.picops.currentDevice.stop()
                        self.picops.currentDevice.unlock_all_buffers()
                    if status == ps.pico_num("PICO_INVALID_TIMEBASE"):
                        self.picops.interval *= 2
                        status = ps.pico_num("PICO_OK")
                self.picops.lastSegment = self.picops.currentSegment
                self.picops.currentSegment += 1
                if self.picops.currentSegment >= self.picops.segments:
                    self.picops.currentSegment = 0
                nowTime = ptime.time()
                lastTime = nowTime - lastTime
                if lastTime > 0:
                    self.emit(self.updateStats, 1 / lastTime)
                lastTime = nowTime
            except Exception as ex:
                print "collector:", ex.message
                continue
            finally:
                # print "collector unlock"
                self.picops.driverAccessLock.release()
                # print "collector unlocked"
            if self.picops.eventDataNeeded.is_set():
                self.picops.eventDataNeeded.clear()
                if status == ps.pico_num("PICO_OK"):
                    if self.picops.deviceKnobStart.isChecked():
                        self.picops.eventDataReady.set()
                else:
                    self.emit(self.startStopReset)
        self.emit(self.finished)

    def plotter(self):
        while self.picops.eventDataReady.wait():
            try:
                if self.picops.eventExit.is_set():
                    break
                if self.picops.currentDevice is None:
                    continue
                segment = self.picops.lastSegment
                timebase = None
                interval = None
                ratio = 1
                if self.picops.eventDataReady.is_set():
                    self.picops.eventDataReady.clear()
                    if self.picops.deviceKnobStart.isChecked():
                        self.picops.eventDataNeeded.set()
                for chan in self.picops.channels:
                    if self.picops.channels[chan].isEnabled():
                        index = self.picops.currentDevice.info.num_channels * segment * 2 + chan * 2
                        status, info = self.picops.currentDevice.get_buffer_info(index)
                        if info is None or len(info) == 0:
                            continue
                        if info["mode"] == self.picops.currentDevice.m.RatioModes.agg:
                            status, ymin, ymax = self.picops.currentDevice.get_min_max_volts(index)
                            if self.picops.timebaseRatioMode == PicoPyRatioModes.max:
                                self.picops.channels[chan].ydata = ymax
                            elif self.picops.timebaseRatioMode == PicoPyRatioModes.minmax:
                                l = min(len(ymin), len(ymax))
                                self.picops.channels[chan].ydata = (ymin[:l] + ymax[:l]) / 2
                            else:
                                self.picops.channels[chan].ydata = ymin
                        else:
                            status, self.picops.channels[chan].ydata = self.picops.currentDevice.get_buffer_volts(index)
                        self.picops.channels[chan].xdata = np.arange(0, len(self.picops.channels[chan].ydata))

                        if (timebase is None or interval is None) and status == ps.pico_num("PICO_OK"):
                            if status == ps.pico_num("PICO_OK"):
                                timebase = info["last_timebase"]
                                interval = info["real_interval"]
                                ratio = info["downsample"]
                self.picops.currentDevice.unlock_all_buffers()
                if self.picops.eventExit.is_set():
                    break
                self.emit(self.plotChannels)
                if self.picops.maxRangeUpdate:
                    for rangei in self.picops.channels[0].rangeMap:
                        if hasattr(self.picops.channels[0].rangeMap[rangei], "enum") \
                                and self.picops.channels[0].rangeMap[rangei].enum == self.picops.maxRange:
                            rangeAbs = self.picops.channels[0].rangeMap[rangei].value
                            self.emit(self.updateYrange, rangeAbs)
                            self.picops.maxRangeUpdate = False
                            break
                if timebase is not None and interval is not None:
                    self.emit(self.updateInterval, interval, timebase, ratio)

            except Exception as ex:
                print "plotter:", ex.message
                continue
            finally:
                pass
                self.picops.app.processEvents()
                pg.QtGui.QApplication.processEvents()
        self.emit(self.finished)

    def generator(self):
        while self.picops.eventSiggenUpdate.wait():
            # print "generator lock"
            self.picops.driverAccessLock.acquire(True)
            # print "generator locked"
            try:
                self.picops.eventSiggenUpdate.clear()
                if self.picops.eventExit.is_set():
                    break
                t, s = self.picops.siggenKnobTypeSelect.itemData(
                    self.picops.siggenKnobTypeSelect.currentIndex()).toInt()
                if self.picops.siggenKnobEnabled.isChecked():
                    status = self.picops.currentDevice. \
                        set_simple_sig_gen(t, self.picops.siggenKnobFrequencySpin.value(),
                                           int(self.picops.siggenKnobPk2pkSpin.value() * 1000000),
                                           int(self.picops.siggenKnobOffsetSpin.value() * 1000000))
                else:
                    status = self.picops.currentDevice. \
                        set_simple_sig_gen(t, self.picops.siggenKnobFrequencySpin.value(), 0, 0)
                if status != ps.pico_num("PICO_OK"):
                    print ps.pico_tag(status)
            except Exception as ex:
                print "generator:", ex.message
            finally:
                # print "generator unlock"
                self.picops.driverAccessLock.release()
                # print "generator unlocked"
                if self.picops.eventExit.is_set():
                    break
        self.emit(self.finished)


class PicoPyRatioModes(psutils.dict2class):
    raw = 0
    min = 1
    max = 2
    minmax = 3
    dec = 4
    avg = 5
    dst = 6
    map = (raw, min, max, minmax, dec, avg, dst)
    labels = {raw: "Raw data", min: "Min data", max: "Max data", minmax: "Min/Max",
              dec: "Decimated", avg: "Average", dst: "Distribution"}
    real = {raw: "raw", min: "agg", max: "agg", minmax: "agg", dec: "dec", avg: "avg", dst: "dst"}

    @staticmethod
    def driverRatioMode(driver, mode):
        for enum in driver.RatioModes.map:
            if PicoPyRatioModes.real[mode] == driver.RatioModes.labels[enum]:
                return enum
        return None


class PicoPyScope(QtGui.QMainWindow):
    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)

        self.app = app
        self.currentDevice = None
        self.lastSegment = 0
        self.currentSegment = 0
        self.maxSegments = 4
        self.segments = self.maxSegments
        self.interval = None
        self.lastInterval = 0
        self.lastTimebase = 0
        self.lastRatio = 1
        self.lastYValue = None
        self.minSamples = 100
        self.maxSamples = 100000
        self.samples = self.maxSamples
        self.maxRange = 0
        self.maxRangeUpdate = False
        self.triggX = None
        self.triggY = None
        self.triggerReset = False
        self.triggerDiamond = None
        self.cpss = 0
        self.cpsc = 0
        self.timebaseKnobTimeRightIndex = 0
        self.timebaseKnobTimeLeftIndex = 0
        self.timebaseRatioMode = PicoPyRatioModes.raw
        self.timebaseRatioReset = True
        self.ratioMode = 0
        self.ratioBin = 1

        self.eventExit = th.Event()
        self.eventExit.clear()
        self.eventDataNeeded = th.Event()
        self.eventDataNeeded.clear()
        self.eventDataReady = th.Event()
        self.eventDataReady.clear()
        self.eventSiggenUpdate = th.Event()
        self.eventSiggenUpdate.clear()
        self.enumDeviceThread = None
        self.selectDeviceThread = None
        self.collectDataThread = None
        self.plotDataThread = None
        self.sigGenThread = None
        self.selectDeviceWorker = None

        self.driverAccessLock = th.Lock()
        self.plotLock = th.Lock()

        self.drivers = {"ps2000": PicoPyDriver("ps2000"),
                        "ps2000a": PicoPyDriver("ps2000a"),
                        "ps3000": PicoPyDriver("ps3000"),
                        "ps3000a": PicoPyDriver("ps3000a"),
                        "ps4000": PicoPyDriver("ps4000"),
                        "ps4000a": PicoPyDriver("ps4000a"),
                        "ps5000a": PicoPyDriver("ps5000a"),
                        "ps6000": PicoPyDriver("ps6000")}

        self._initUI()
        self._initWorkers()

    def closeEvent(self, event):
        self.eventExit.set()
        self.eventDataNeeded.set()
        self.eventDataReady.set()
        self.eventSiggenUpdate.set()
        self._exitStub(False)

    def _exitStub(self, loop=True):
        if True in ((t is not None and t.isRunning()) for t in (self.enumDeviceThread, self.selectDeviceThread,
                                                                self.collectDataThread, self.plotDataThread,
                                                                self.sigGenThread)):
            QtCore.QTimer.singleShot(100, self._exitStub)
        if not loop:
            exit(0)

    def _initUI(self):
        pg.setConfigOptions(antialias=False)
        dock = DockArea()
        dock.setParent(self)
        dock.setObjectName("main_dock")
        self.setCentralWidget(dock)
        self.resize(600, 400)
        self.setWindowTitle("PicoPyScope")

        self.times = {
            0: {'label': '5\265s', 'interval': 5000},
            1: {'label': '1ms', 'interval': 1000000},
            2: {'label': '2ms', 'interval': 2000000},
            3: {'label': '5ms', 'interval': 5000000},
            4: {'label': '10ms', 'interval': 10000000},
            5: {'label': '20ms', 'interval': 20000000},
            6: {'label': '50ms', 'interval': 50000000},
            7: {'label': '100ms', 'interval': 100000000},
            8: {'label': '200ms', 'interval': 200000000},
            9: {'label': '500ms', 'interval': 500000000},
            10: {'label': '1s', 'interval': 1000000000},
        }

        self.scopeView = Dock("Scope View", area=None, size=(200, 150), widget=None, hideTitle=False,
                              autoOrientation=False)
        self.viewPlot = pg.PlotWidget(title=None, autoDownsample=True)
        self.scopeView.addWidget(self.viewPlot)
        self.viewPlotItem = self.viewPlot.getPlotItem()
        # self.viewPlotItem.setDownsampling(ds=True, auto=True, mode="subsample")
        self.viewPlotItem.setTitle(title="<font size=1>.</font>", justify='right')
        self.viewBox = self.viewPlotItem.getViewBox()
        self.viewBox.setMouseMode(pg.ViewBox.RectMode)
        self.viewPlotItem.setLabel(axis='left', text=None, units='V')
        self.viewPlotItem.setLabel(axis='bottom', text=None, units='s')
        self.viewPlotItem.showGrid(True, True, 0.7)
        # self.viewPlot.setBackground((242,242,232))
        self.viewPlot.setAspectLocked(False)
        self.viewPlotXaxis = self.viewPlotItem.getAxis('bottom')
        self.viewPlotYaxis = self.viewPlotItem.getAxis('left')

        self.channels = {}
        for chan in range(2):
            self.channels[chan] = PicoPyChannel(chan)

        if self.plotLock.acquire(False):
            self.plotLock.release()

        self.deviceKnob = Dock("PS Device", area=None, size=(200, 50), widget=None, hideTitle=False,
                               autoOrientation=False)
        self.deviceKnob.setFixedSize(200, 100)
        self.deviceKnobWidget = pg.LayoutWidget()
        self.deviceKnob.addWidget(self.deviceKnobWidget, row=0, col=0)

        self.deviceKnobSelect = QtGui.QComboBox()
        self.deviceKnobWidget.addWidget(self.deviceKnobSelect, row=0, col=0, colspan=2)
        self.deviceKnobSelect.addItem("None", userData=None)
        self.deviceKnobSelect.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.deviceKnobSelect.currentIndexChanged.connect(self.deviceKnobSelectChange)

        self.deviceKnobStart = QtGui.QPushButton("Start")
        self.deviceKnobWidget.addWidget(self.deviceKnobStart, row=1, col=0)
        self.deviceKnobStart.setCheckable(True)
        self.deviceKnobStart.clicked[bool].connect(self.deviceKnobStartClicked)

        self.deviceKnobStop = QtGui.QPushButton("Stop")
        self.deviceKnobWidget.addWidget(self.deviceKnobStop, row=1, col=1)
        self.deviceKnobStop.setCheckable(True)
        self.deviceKnobStop.clicked[bool].connect(self.deviceKnobStopClicked)

        self.deviceKnobStartStopReset()

        self.deviceKnobFreeze(True)

        self.siggenKnob = Dock("Sig Gen", area=None, size=(200, 50), widget=None, hideTitle=False,
                               autoOrientation=False)
        self.siggenKnob.setFixedSize(200, 110)
        self.siggenKnobWidget = pg.LayoutWidget()
        self.siggenKnob.addWidget(self.siggenKnobWidget, row=0, col=0)

        self.siggenKnobTypeLabel = QtGui.QLabel("Type:")
        self.siggenKnobTypeLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.siggenKnobWidget.addWidget(self.siggenKnobTypeLabel, row=0, col=1, rowspan=1, colspan=50)

        self.siggenKnobFrequencyLabel = QtGui.QLabel("Frequency:")
        self.siggenKnobFrequencyLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.siggenKnobWidget.addWidget(self.siggenKnobFrequencyLabel, row=0, col=51, rowspan=1, colspan=50)

        self.siggenKnobEnabled = QtGui.QCheckBox("")
        self.siggenKnobEnabled.stateChanged.connect(self.siggenEnabled)
        self.siggenKnobWidget.addWidget(self.siggenKnobEnabled, row=1, col=0, rowspan=1, colspan=1)

        self.siggenKnobTypeSelect = QtGui.QComboBox()
        self.siggenKnobTypeSelect.currentIndexChanged.connect(self.siggenUpdate)
        self.siggenKnobWidget.addWidget(self.siggenKnobTypeSelect, row=1, col=1, rowspan=1, colspan=50)

        self.siggenKnobFrequencySpin = pg.SpinBox(value=1000, dec=True, step=0.5, minStep=0.1, bounds=[1, 1e6],
                                                  suffix='Hz', siPrefix=True)
        self.siggenKnobFrequencySpin.valueChanged.connect(self.siggenUpdate)
        self.siggenKnobWidget.addWidget(self.siggenKnobFrequencySpin, row=1, col=51, rowspan=1, colspan=50)

        self.siggenKnobPk2pkLabel = QtGui.QLabel("Pk2pk:")
        self.siggenKnobPk2pkLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.siggenKnobWidget.addWidget(self.siggenKnobPk2pkLabel, row=2, col=1, rowspan=1, colspan=50)

        self.siggenKnobOffsetLabel = QtGui.QLabel("Offset:")
        self.siggenKnobOffsetLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.siggenKnobWidget.addWidget(self.siggenKnobOffsetLabel, row=2, col=51, rowspan=1, colspan=50)

        self.siggenKnobPk2pkSpin = pg.SpinBox(value=1, dec=True, step=0.01, minStep=1e-2, bounds=[0, 4], suffix='V',
                                              siPrefix=True)
        self.siggenKnobPk2pkSpin.valueChanged.connect(self.siggenUpdate)
        self.siggenKnobWidget.addWidget(self.siggenKnobPk2pkSpin, row=3, col=1, rowspan=1, colspan=50)

        self.siggenKnobOffsetSpin = pg.SpinBox(value=0, dec=True, step=0.01, minStep=1e-2, bounds=[-4, 4], suffix='V',
                                               siPrefix=True)
        self.siggenKnobOffsetSpin.valueChanged.connect(self.siggenUpdate)
        self.siggenKnobWidget.addWidget(self.siggenKnobOffsetSpin, row=3, col=51, rowspan=1, colspan=50)

        self.siggenKnobEnabled.setChecked(False)
        self.siggenEnabled(False)

        self.triggerKnob = Dock("Trigger", area=None, size=(200, 20), widget=None, hideTitle=False,
                                autoOrientation=False)
        self.triggerKnob.setFixedSize(200, 65)
        self.triggerKnobWidget = pg.LayoutWidget()
        self.triggerKnob.addWidget(self.triggerKnobWidget, row=0, col=0)
        self.triggerKnobEnabled = QtGui.QCheckBox("")
        self.triggerKnobWidget.addWidget(self.triggerKnobEnabled, row=1, col=0, rowspan=1, colspan=1)

        self.triggerKnobSourceLabel = QtGui.QLabel("Source:")
        self.triggerKnobSourceLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.triggerKnobWidget.addWidget(self.triggerKnobSourceLabel, row=0, col=1, rowspan=1, colspan=50)

        self.triggerKnobSource = QtGui.QComboBox()
        self.triggerKnobSource.currentIndexChanged.connect(self.triggerKnobSourceChange)
        self.triggerKnobWidget.addWidget(self.triggerKnobSource, row=1, col=1, rowspan=1, colspan=50)

        self.triggerKnobDirectionLabel = QtGui.QLabel("Direction:")
        self.triggerKnobDirectionLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.triggerKnobWidget.addWidget(self.triggerKnobDirectionLabel, row=0, col=52, rowspan=1, colspan=50)

        self.triggerKnobDirection = QtGui.QComboBox()
        self.triggerKnobDirection.currentIndexChanged.connect(self.triggerKnobDirectionChange)

        self.triggerKnobWidget.addWidget(self.triggerKnobDirection, row=1, col=52, rowspan=1, colspan=50)

        self.triggerDiamond = None

        self.triggerKnobEnabled.stateChanged.connect(self.triggerKnobEnabledChange)
        self.triggerKnobEnabled.setChecked(False)
        self.triggerKnobEnabledChange(False)

        self.timebaseKnob = Dock("Timebase", area=None, size=(200, 20), widget=None, hideTitle=False,
                                 autoOrientation=False)
        self.timebaseKnob.setFixedSize(200, 140)
        self.timebaseKnobWidget = pg.LayoutWidget()
        self.timebaseKnob.addWidget(self.timebaseKnobWidget, row=0, col=0)
        self.timebaseKnobTimeValueLabel = QtGui.QLabel("")
        self.timebaseKnobTimeValueLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom))
        self.timebaseKnobTime = QtGui.QScrollBar(QtCore.Qt.Horizontal)
        self.timebaseKnobTime.valueChanged.connect(self.timebaseKnobTimeChange)
        self.timebaseKnobTimeLeftIndex = 5
        self.timebaseKnobTimeLeftLabel = QtGui.QLabel(self.times[self.timebaseKnobTimeLeftIndex]["label"])
        self.timebaseKnobTimeLeftLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop))
        self.timebaseKnobTimeRightIndex = 7
        self.timebaseKnobTimeRightLabel = QtGui.QLabel(self.times[self.timebaseKnobTimeRightIndex]["label"])
        self.timebaseKnobTimeRightLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop))
        self.timebaseKnobTime.setRange(0, 60)
        self.timebaseKnobTime.setValue(30)
        self.timebaseKnobRatioModeLabel = QtGui.QLabel("Ratio Mode")
        self.timebaseKnobRatioModeLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.timebaseKnobRatioMode = QtGui.QComboBox()
        for m in PicoPyRatioModes.map:
            self.timebaseKnobRatioMode.addItem(PicoPyRatioModes.labels[m], userData=m)
        self.timebaseKnobRatioMode.currentIndexChanged.connect(self.timebaseKnobRatioModeChange)
        self.timebaseKnobRatioMode.setCurrentIndex(self.timebaseRatioMode)
        self.timebaseKnobRatioBinLabel = QtGui.QLabel("Value")
        self.timebaseKnobRatioBinLabel.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom))
        self.timebaseKnobRatioBin = \
            pg.SpinBox(value=1, dec=False, step=1, minStep=1, bounds=[1, 10], suffix='', siPrefix=False, decimals=False)
        self.timebaseKnobRatioBin.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom))
        self.timebaseKnobRatioBin.sigValueChanged.connect(self.timebaseKnobRatioBinChange)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobTimeValueLabel, row=0, col=1, rowspan=1, colspan=2)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobTime, row=1, col=0, rowspan=1, colspan=4)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobTimeLeftLabel, row=2, col=0, rowspan=1, colspan=1)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobTimeRightLabel, row=2, col=3, rowspan=1, colspan=1)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobRatioModeLabel, row=3, col=0, rowspan=1, colspan=2)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobRatioBinLabel, row=3, col=2, rowspan=1, colspan=2)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobRatioMode, row=4, col=0, rowspan=1, colspan=2)
        self.timebaseKnobWidget.addWidget(self.timebaseKnobRatioBin, row=4, col=2, rowspan=1, colspan=2)

        self.dock0 = Dock("Dock 0", area=None, widget=None, hideTitle=True, autoOrientation=False)
        self.dock0.hStyle = self.dock0.vStyle = self.dock0.nStyle = self.dock0.dragStyle = """
        Dock > QWidget {
            border: 0px solid #000;
        }"""

        dock.addDock(self.scopeView, positon='top', relativeTo=None)
        dock.addDock(self.deviceKnob, position='right', relativeTo=self.scopeView)
        dock.addDock(self.siggenKnob, position='bottom', relativeTo=self.deviceKnob)
        dock.addDock(self.triggerKnob, position='bottom', relativeTo=self.siggenKnob)
        dock.addDock(self.timebaseKnob, position='bottom', relativeTo=self.triggerKnob)
        dock.addDock(self.dock0, position='bottom', relativeTo=self.timebaseKnob)
        dock.addDock(self.channels[0].dock, position='bottom', relativeTo=None)
        dock.addDock(self.channels[1].dock, position='right', relativeTo=self.channels[0].dock)
        self.offUI()

    def channelsPopulate(self):
        if self.currentDevice is None or self.currentDevice.info is None:
            return
        dock = self.findChild(DockArea, name="main_dock")
        if dock is None:
            return
        if self.currentDevice.info.num_channels > len(self.channels):
            for chan in range(len(self.channels), self.currentDevice.info.num_channels):
                self.channels[chan] = PicoPyChannel(chan)
                if chan < 4:
                    dock.addDock(self.channels[chan].dock, position='right', realtiveTo=self.channels[chan - 1].dock)
                    dock.moveDock(self.channels[chan].dock, position='right', neighbor=self.channels[chan - 1].dock)
                else:
                    dock.addDock(self.channels[chan].dock, position='bottom', realtiveTo=self.channels[chan - 4].dock)
                    dock.moveDock(self.channels[chan].dock, position='bottom', neighbor=self.channels[chan - 4].dock)
        elif self.currentDevice.info.num_channels < len(self.channels):
            for chan in range(len(self.channels) - 1, self.currentDevice.info.num_channels - 1, -1):
                self.channels[chan].dock.setParent(None)
                del (self.channels[chan])

        self.siggenKnobTypeSelect.clear()
        if self.currentDevice.info.has_siggen:
            for wave in self.currentDevice.m.WaveTypes.map:
                self.siggenKnobTypeSelect.addItem(self.currentDevice.m.WaveTypes.labels[wave], userData=wave)
            self.siggenKnobFrequencySpin.setMaximum(self.currentDevice.info.siggen_frequency)

        if self.siggenKnobEnabled.isChecked() and not self.currentDevice.info.has_siggen:
            self.siggenKnobEnabled.setChecked(False)
            self.siggenEnabled(False)

        self.triggerKnobSource.clear()
        self.triggerKnobSource.addItem("None")
        for chan in self.channels:
            self.channels[chan].loadRanges(self.currentDevice.info.channel_ranges)
            self.channels[chan].freeze(False)
            self.channels[chan].enum = self.currentDevice.m.Channels.map[chan]
            self.triggerKnobSource.addItem(self.channels[chan].shortName)

        self.triggerKnobDirection.clear()
        for d in self.currentDevice.m.ThresholdDirections.simple:
            self.triggerKnobDirection.addItem(self.currentDevice.m.ThresholdDirections.labels[d], userData=d)

        self.timebaseKnobRatioMode.clear()
        for m in PicoPyRatioModes.map:
            if PicoPyRatioModes.driverRatioMode(self.currentDevice.m, m) in self.currentDevice.m.RatioModes.map:
                self.timebaseKnobRatioMode.addItem(PicoPyRatioModes.labels[m], userData=m)

    def channelPlot(self):
        if self.plotLock.acquire(False):
            try:
                for chan in self.channels:
                    if self.channels[chan].isEnabled():
                        if self.channels[chan].plot is None:
                            self.channels[chan].plot = self.viewPlotItem.plot(pen=self.channels[chan].pen)
                        self.channels[chan].draw()
                    else:
                        if self.channels[chan].plot is not None:
                            self.viewPlotItem.removeItem(self.channels[chan].plot)
                            self.channels[chan].plot.setParent(None)
                            self.channels[chan].plot = None
                            # if anyOn:
                            #    nowTime = ptime.time()
                            #    div = nowTime - self.lastTime
                            #    if div != 0:
                            #        self.fps = 1 / div
                            #        self.lastTime = nowTime
                            #        self.statsUpdate(0.0, True)
            except Exception as ex:
                print "channelPlot", ex.message
            finally:
                self.plotLock.release()

    def statsUpdate(self, value):
        if self.cpsc < 10:
            self.cpss += float(value)
            self.cpsc += 1
        else:
            self.viewPlotItem.setTitle(title="<font size=2>%2.2f cps</font>" % float(self.cpss / self.cpsc))
            self.cpsc = 0
            self.cpss = 0.0

    def deviceKnobFreeze(self, state):
        self.deviceKnob.setEnabled(not state)

    def deviceKnobSelectChange(self, index):
        if index >= 0:
            self.selectDeviceThread = QtCore.QThread()
            self.selectDeviceWorker = PicoPyDeviceWorker(self)
            self.connect(self.selectDeviceWorker, self.selectDeviceWorker.finished, self.selectDeviceThread.quit)
            self.connect(self.selectDeviceWorker, self.selectDeviceWorker.freezeUI, self.freezeUI)
            self.connect(self.selectDeviceWorker, self.selectDeviceWorker.startStopReset, self.deviceKnobStartStopReset)
            self.connect(self.selectDeviceWorker, self.selectDeviceWorker.freezeDeviceKnob, self.deviceKnobFreeze)
            self.selectDeviceWorker.moveToThread(self.selectDeviceThread)
            if index > 0:
                self.selectDeviceThread.started.connect(self.selectDeviceWorker.opener)
                self.connect(self.selectDeviceWorker, self.selectDeviceWorker.popChannels, self.channelsPopulate)
            else:
                self.selectDeviceThread.started.connect(self.selectDeviceWorker.closer)
            self.selectDeviceThread.finished.connect(self.selectDeviceWorker.deleteLater)
            self.selectDeviceThread.start()

    def deviceKnobStartClicked(self, state):
        # print "Start Clicked %s" % ("in" if state else "out")
        if state:
            self.deviceKnobStart.setEnabled(False)
            self.deviceKnobStop.setEnabled(True)
            self.deviceKnobStop.setChecked(False)
            self.eventDataNeeded.set()
        pass

    def deviceKnobStopClicked(self, state):
        # print "Stop Clicked %s" % ("in" if state else "out")
        if state:
            self.deviceKnobStop.setEnabled(False)
            self.deviceKnobStart.setEnabled(True)
            self.deviceKnobStart.setChecked(False)
            self.eventDataNeeded.clear()
            self.eventDataReady.clear()
        pass

    def deviceKnobStartStopReset(self):
        # print "Resetting start/stop"
        self.deviceKnobStart.setEnabled(True)
        self.deviceKnobStart.setChecked(False)
        self.deviceKnobStop.setEnabled(False)
        self.deviceKnobStop.setChecked(True)

    def siggenEnabled(self, state):
        for widget in [self.siggenKnobTypeSelect, self.siggenKnobFrequencySpin, self.siggenKnobPk2pkSpin,
                       self.siggenKnobOffsetSpin]:
            widget.setEnabled(state)
        self.siggenUpdate()

    def siggenUpdate(self):
        if self.currentDevice is not None and self.currentDevice.info.has_siggen:
            self.eventSiggenUpdate.set()

    def triggerKnobSourceChange(self, index):
        self.triggerReset = True

    def triggerKnobDirectionChange(self, index):
        self.triggerReset = True

    def triggerKnobEnabledChange(self, state):
        self.triggerKnobSource.setEnabled(state)
        self.triggerKnobDirection.setEnabled(state)
        if state:
            if self.triggX is None:
                self.triggX = 0.5
            if self.triggY is None:
                self.triggY = 0
            if self.triggerDiamond is None:
                self.triggerDiamond = pg.RectROI([self.triggX * self.samples / self.ratioBin, self.triggY],
                                                 [0, 0], invertible=True, pen=pg.mkPen(None))
                self.triggerDiamond.sigRegionChanged.connect(self.triggerDiamondUpdate)
                self.viewPlot.addItem(self.triggerDiamond)
        else:
            self.viewPlot.removeItem(self.triggerDiamond)
            self.triggerDiamond = None
        self.triggerReset = True

    def triggerDiamondUpdate(self, roi, reset=True):
        # xpos, ypos = roi.pos()
        xsize, ysize = roi.size()
        if self.lastRatio is None or self.lastRatio == 0:
            self.lastRatio = 1
        self.triggX += xsize * self.lastRatio / self.samples
        self.triggY += ysize
        # print xpos, ypos, xsize, ysize, self.triggX, self.triggY, reset
        if reset:
            self.triggerReset = True
            roi.setPos([self.triggX * self.samples / self.lastRatio, self.triggY], update=False, finish=False)
            roi.setSize([0, 0], update=False, finish=False)
            self.triggerDiamondUpdate(roi, False)

    def timebaseKnobTimeChange(self, value):
        reinit = False
        last = self.interval
        if value < 5:
            # print "decrease range"
            if self.timebaseKnobTimeLeftIndex > 0:
                reinit = True
                # print "shift both by 1 down"
                self.timebaseKnobTimeLeftIndex -= 1
                self.timebaseKnobTimeRightIndex = self.timebaseKnobTimeLeftIndex + 2
            else:
                if self.timebaseKnobTimeRightIndex == self.timebaseKnobTimeLeftIndex + 2:
                    reinit = True
                    # print "shift only right by 1 down"
                    self.timebaseKnobTimeRightIndex -= 1
                else:
                    # print "do nothing"
                    pass
        elif value > 55:
            # print "increase range"
            if self.timebaseKnobTimeRightIndex < len(self.times) - 1:
                reinit = True
                # print "shift both by 1 up"
                self.timebaseKnobTimeRightIndex += 1
                self.timebaseKnobTimeLeftIndex = self.timebaseKnobTimeRightIndex - 2
            else:
                if self.timebaseKnobTimeLeftIndex == self.timebaseKnobTimeRightIndex - 2:
                    reinit = True
                    # print "shift only left by 1 up"
                    self.timebaseKnobTimeLeftIndex += 1
                else:
                    # print "do nothing"
                    pass
        else:
            # print "inside"
            pass
        if reinit:
            # print "r e l o a d"
            state = self.timebaseKnobTime.isEnabled()
            if state:
                self.timebaseKnobTime.setEnabled(False)
            self.timebaseKnobTimeLeftLabel.setText(self.times[self.timebaseKnobTimeLeftIndex]["label"])
            self.timebaseKnobTimeRightLabel.setText(self.times[self.timebaseKnobTimeRightIndex]["label"])
            newValue = int(60.0 * (last - self.times[self.timebaseKnobTimeLeftIndex]["interval"]) / (
                self.times[self.timebaseKnobTimeRightIndex]["interval"] - self.times[self.timebaseKnobTimeLeftIndex][
                    "interval"]))
            self.timebaseKnobTime.setValue(newValue)
            self.triggerReset = True
            if state:
                self.timebaseKnobTime.setEnabled(True)
            return
        self.interval = \
            self.times[self.timebaseKnobTimeLeftIndex]["interval"] + \
            (value / 60.0) * \
            (self.times[self.timebaseKnobTimeRightIndex]["interval"] -
             self.times[self.timebaseKnobTimeLeftIndex]["interval"])
        if last is None:
            self.timebaseKnobTimeValueLabel.setText("%s " % pg.siFormat(int(self.interval) / 1000000000.0, suffix="s"))

    def timebaseKnobRatioModeChange(self, index):
        if index is None:
            index = self.timebaseKnobRatioMode.currentIndex()
        mode = self.timebaseKnobRatioMode.itemData(index).toInt()[0]
        if mode == PicoPyRatioModes.raw:
            self.timebaseKnobRatioBin.setEnabled(False)
            self.timebaseKnobRatioBin.setMinimum(1, update=False)
            self.timebaseKnobRatioBin.setValue(1)
        else:
            if self.timebaseKnobRatioBin.value() == 1:
                self.timebaseKnobRatioBin.setValue(2)
                self.timebaseKnobRatioBin.setMinimum(2, update=False)
            if not self.timebaseKnobRatioBin.isEnabled():
                self.timebaseKnobRatioBin.setEnabled(True)
        self.timebaseRatioReset = True

    def timebaseKnobRatioBinChange(self):
        self.timebaseRatioReset = True

    def onOffUI(self, state):
        for dock in (self.scopeView, self.deviceKnobStart, self.deviceKnobStop,
                     self.siggenKnob, self.triggerKnob, self.timebaseKnob):
            dock.setEnabled(state)
        for chan in self.channels:
            self.channels[chan].freeze(not state)
        if state:
            self.timebaseKnobRatioModeChange(None)

    def onUI(self):
        self.onOffUI(True)

    def offUI(self):
        self.onOffUI(False)

    def freezeUI(self, state):
        self.onOffUI(not state)

    def rangeYUpdate(self, value):
        # self.viewPlot.setXRange(min=0, max=self.samples / self.ratioBin, padding=0)
        self.viewPlot.setYRange(min=-value, max=value)
        self.viewPlot.setLimits(yMin=-value * 1.25, yMax=value * 1.25)

    def intervalUpdate(self, interval, timebase, ratio):
        if self.lastInterval != interval \
                or (timebase != 0 and self.lastTimebase != timebase) \
                or self.lastRatio != ratio:
            if self.lastTimebase != timebase or self.lastRatio != ratio:
                (x1, y1, x2, y2) = self.viewPlot.viewRect().getCoords()
                self.viewPlotXaxis.setScale(ratio * interval / 1000000000.0)
                lim = self.samples / ratio
                if self.lastInterval is not None and self.lastInterval != 0 \
                        and self.lastRatio is not None and self.lastRatio != 0 and ratio != 0 and interval != 0 \
                        and x2 != self.samples / self.lastRatio:
                    r = float(self.lastRatio * self.lastInterval) / float(ratio * interval)
                    self.viewPlot.setXRange(min=(r * x1), max=min((r * x2), lim), padding=0)
                else:
                    self.viewPlot.setXRange(min=0, max=lim, padding=0)
                self.viewPlot.setLimits(xMin=0, xMax=lim)
                if timebase > 0:
                    self.lastTimebase = timebase
                if self.lastRatio != ratio:
                    self.lastRatio = ratio
                if self.lastInterval != interval:
                    self.timebaseKnobTimeValueLabel.setText(
                        "%s " % pg.siFormat(interval * self.samples / 1000000000.0, suffix="s"))
                    self.lastInterval = interval
                if self.triggerDiamond is not None:
                    self.triggerDiamondUpdate(self.triggerDiamond, True)

    def _initWorkers(self):
        if self.driverAccessLock.acquire(False):
            self.driverAccessLock.release()

        self.enumDeviceThread = QtCore.QThread()
        self.enumDeviceWorker = PicoPyDeviceWorker(self)
        self.connect(self.enumDeviceWorker, self.enumDeviceWorker.finished, self.enumDeviceThread.quit)
        self.connect(self.enumDeviceWorker, self.enumDeviceWorker.freezeDeviceKnob, self.deviceKnobFreeze)
        self.enumDeviceWorker.moveToThread(self.enumDeviceThread)
        self.enumDeviceThread.started.connect(self.enumDeviceWorker.enumerator)
        self.enumDeviceThread.finished.connect(self.enumDeviceWorker.deleteLater)
        self.enumDeviceThread.start()

        self.collectDataThread = QtCore.QThread()
        self.collectDataWorker = PicoPyDeviceWorker(self)
        self.connect(self.collectDataWorker, self.collectDataWorker.finished, self.collectDataThread.quit)
        self.connect(self.collectDataWorker, self.collectDataWorker.startStopReset, self.deviceKnobStartStopReset)
        self.connect(self.collectDataWorker, self.collectDataWorker.updateStats, self.statsUpdate)
        self.collectDataWorker.moveToThread(self.collectDataThread)
        self.collectDataThread.started.connect(self.collectDataWorker.collector)
        self.collectDataThread.finished.connect(self.collectDataWorker.deleteLater)
        self.collectDataThread.start()

        self.plotDataThread = QtCore.QThread()
        self.plotDataWorker = PicoPyDeviceWorker(self)
        self.connect(self.plotDataWorker, self.plotDataWorker.updateYrange, self.rangeYUpdate)
        self.connect(self.plotDataWorker, self.plotDataWorker.updateInterval, self.intervalUpdate)
        # self.connect(self.plotDataWorker, self.plotDataWorker.drawChannel, self.channelDraw)
        # self.connect(self.plotDataWorker, self.plotDataWorker.downChannel, self.channelDown)
        self.connect(self.plotDataWorker, self.plotDataWorker.plotChannels, self.channelPlot)
        self.connect(self.plotDataWorker, self.plotDataWorker.finished, self.plotDataThread.quit)
        self.plotDataWorker.moveToThread(self.plotDataThread)
        self.plotDataThread.started.connect(self.plotDataWorker.plotter)
        self.plotDataThread.finished.connect(self.plotDataWorker.deleteLater)
        self.plotDataThread.start()

        self.sigGenThread = QtCore.QThread()
        self.sigGenWorker = PicoPyDeviceWorker(self)
        self.connect(self.sigGenWorker, self.sigGenWorker.finished, self.sigGenThread.quit)
        self.sigGenWorker.moveToThread(self.sigGenThread)
        self.sigGenThread.started.connect(self.sigGenWorker.generator)
        self.sigGenThread.finished.connect(self.sigGenWorker.deleteLater)
        self.sigGenThread.start()


def main():
    app = QtGui.QApplication([])
    win = PicoPyScope(app)
    win.show()
    # debug = pg.dbg()
    try:
        sys.exit(app.exec_())
    except Exception as ex:
        print "main:", ex.message


if __name__ == '__main__':
    main()
