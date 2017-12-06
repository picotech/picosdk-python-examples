# -*- coding: utf-8 -*-
#
# Copyright (C) 2014-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Python calls for ps5000 based PicoScope devices.
"""

from threading import *
from picostatus import *
from psutils import *
from math import ceil
from copy import deepcopy
import numpy as np
import sys
import time

"""
Defaults
"""
MAX_INFO_LEN = 64
MAX_NUM_DEVICES = 64
MAX_LOGIC_LEVEL = 32767
MIN_LOGIC_LEVEL = -32767
MAX_LOGIC_VOLTS = 5
STREAM_LENGTH = 1000000


class UnitInfo(dict2class):
    """ Place holder type for device information """
    pass


class Channels(dict2class):
    """ Class defining channels for the current device class """
    A = 0
    B = 1
    C = 2
    D = 3
    map = (A, B, C, D)
    labels = {A: "A", B: "B", C: "C", D: "D"}


class ChannelState(dict2class):
    """ Object describing state of the channel """

    def __init__(self):
        self.enabled = False
        self.coupling = Couplings.dc
        self.range = Ranges.r500mv
        self.offset = 0
        self.overvoltaged = False


class Couplings(dict2class):
    """ Couplings selection """
    ac = 0
    dc = 1
    labels = {ac: "AC", dc: "DC"}


class Ports(dict2class):
    """ Device digital ports selection """
    p0 = 0x80
    p1 = 0x81
    p2 = 0x82
    p3 = 0x83
    map = (p0, p1, p2, p3)
    labels = {p0: "p0", p1: "p1", p2: "p2", p3: "p3"}


class PortState(dict2class):
    """ Object describing state of the digital port """

    def __init__(self):
        self.enabled = False
        self.level = 0


class PortBits(dict2class):
    """ Bits numbers used in MSO collections """
    b0 = 0
    b1 = 1
    b2 = 2
    b3 = 3
    b4 = 4
    b5 = 5
    b6 = 6
    b7 = 7
    b8 = 8
    b9 = 9
    b10 = 10
    b11 = 11
    b12 = 12
    b13 = 13
    b14 = 14
    b15 = 15
    b16 = 16
    b17 = 17
    b18 = 18
    b19 = 19
    b20 = 20
    b21 = 21
    b22 = 22
    b23 = 23
    b24 = 24
    b25 = 25
    b26 = 26
    b27 = 27
    b28 = 28
    b29 = 29
    b30 = 30
    b31 = 31
    map = ((b0, b1, b3, b3, b4, b5, b6, b7), (b8, b9, b10, b11, b12, b13, b14, b15),
           (b16, b17, b18, b19, b20, b21, b22, b23), (b24, b25, b26, b27, b28, b29, b30, b31))
    portmap = {
        Ports.p0: (b0, b1, b3, b3, b4, b5, b6, b7),
        Ports.p1: (b8, b9, b10, b11, b12, b13, b14, b15),
        Ports.p2: (b16, b17, b18, b19, b20, b21, b22, b23),
        Ports.p3: (b24, b25, b26, b27, b28, b29, b30, b31)
    }
    labels = {0: "b0", 1: "b1", 2: "b2", 3: "b3", 4: "b4", 5: "b5", 6: "b6", 7: "b7",
              8: "b8", 9: "b9", 10: "b10", 11: "b11", 12: "b12", 13: "b13", 14: "b14", 15: "b15",
              16: "b16", 17: "b17", 18: "b18", 19: "b19", 20: "b20", 21: "b21", 22: "b22", 23: "b23",
              24: "b24", 25: "b25", 26: "b26", 27: "b27", 28: "b28", 29: "b29", 30: "b30", 31: "b31"}


class Ranges(dict2class):
    """ Universal class with channel ranges """
    r10mv = 0
    r20mv = 1
    r50mv = 2
    r100mv = 3
    r200mv = 4
    r500mv = 5
    r1v = 6
    r2v = 7
    r5v = 8
    r10v = 9
    r20v = 10
    r50v = 11
    r100v = 12
    r200v = 13
    r400v = 14
    map = (r10mv, r20mv, r50mv, r100mv, r200mv, r500mv, r1v, r2v, r5v, r10v, r20v, r50v, r100v, r200v, r400v)
    labels = {r10mv: "\26110mV", r20mv: "\26120mV", r50mv: "\26150mV",
              r100mv: "\261100mV", r200mv: "\261200mV", r500mv: "\261500mV",
              r1v: "\2611V", r2v: "\2612V", r5v: "\2615V",
              r10v: "\26110V", r20v: "\26120V", r50v: "\26150V",
              r100v: "\261100V", r200v: "\261200V", r400v: "\261400V"}
    values = {r10mv: 0.01, r20mv: 0.02, r50mv: 0.05,
              r100mv: 0.1, r200mv: 0.2, r500mv: 0.5,
              r1v: 1.0, r2v: 2.0, r5v: 5.0,
              r10v: 10.0, r20v: 20.0, r50v: 50.0,
              r100v: 100.0, r200v: 200.0, r400v: 400.0}
    ascii_labels = {r10mv: "+/-10mV", r20mv: "+/-20mV", r50mv: "+/-50mV",
                    r100mv: "+/-100mV", r200mv: "+/-200mV", r500mv: "+/-500mV",
                    r1v: "+/-1V", r2v: "+/-2V", r5v: "+/-5V",
                    r10v: "+/-10V", r20v: "+/-20V", r50v: "+/-50V",
                    r100v: "+/-100V", r200v: "+/-200V", r400v: "+/-400V"}


class RatioModes(dict2class):
    """ Collection of reduction modes """
    raw = 0
    none = raw
    agg = 1
    aggregate = agg
    dec = 2
    decimate = dec
    avg = 4
    average = avg
    map = (raw, agg, dec, avg)
    labels = {raw: "raw", agg: "agg", dec: "dec", avg: "avg"}

    @staticmethod
    def mode2dict(mode):
        """ Returns dict of matched modes
        :param mode: OR-ed modes selection
        :type mode: int
        :return: dict of valid labels with enum values
        :rtype: dict
        """
        r = {}
        for m in RatioModes.labels:
            if mode == m:
                return {RatioModes.labels[m]: m}
            if mode & m > 0:
                r[RatioModes.labels[m]] = m
        return r

    @staticmethod
    def isvalid(mode):
        """ Quick test, whether provided mode is a valid one
        :param mode: OR-ed modes selection to validate
        :type mode: int
        :return: if valid
        :rtype: bool
        """
        return len(RatioModes.mode2dict(mode)) > 0

    @staticmethod
    def issingle(mode):
        return mode in RatioModes.labels.keys()


class BufferInfo(dict2class):
    """ Type specifier for Block Buffer structure """

    def __init__(self):
        self.access_lock = Lock()


class ThresholdModes(dict2class):
    """ Simple trigger threshold collection """
    lvl = 0
    level = lvl
    win = 1
    window = win
    map = (lvl, win)
    labels = {lvl: "level", win: "window"}


class SweepTypes(dict2class):
    """ Collection of Sweep Types in Simple Signal Generator """
    up = 0
    down = 1
    updown = 2
    downup = 3
    map = (up, down, updown, downup)
    labels = {up: "up", down: "down", updown: "updown", downup: "downup"}


class WaveTypes(dict2class):
    """ Collection of Waveform Types for Simple Signal Generator """
    sine = 0
    square = 1
    triangle = 2
    ramp_up = 3
    ramp_down = 4
    sinc = 5
    gaussian = 6
    half_sine = 7
    dc = 8
    map = (sine, square, triangle, ramp_up, ramp_down, sinc, gaussian, half_sine, dc)
    labels = {sine: "sine", square: "square", triangle: "triangle", ramp_up: "ramp up", ramp_down: "ramp down",
              sinc: "sinc", gaussian: "gaussian", half_sine: "half sine", dc: "DC"}


class SigExtra(dict2class):
    """ Collection of additionall parameters for Advanced Signal Generator """
    off = 0
    white_noise = 1
    wnoise = white_noise
    prbs = 2
    map = (off, wnoise, prbs)
    labels = {off: "off", wnoise: "white noise", prbs: "PRBS"}


class SigTriggerTypes(dict2class):
    """ Collection of Trigger Types for Advanced Signal Generator """
    rising = 0
    falling = 1
    gate_high = 2
    gate_low = 3
    map = (rising, falling, gate_high, gate_low)
    labels = {rising: "rising", falling: "falling", gate_high: "gate high", gate_low: "gate low"}


class SigTriggerSource(dict2class):
    """ Collection of Trigger Sources for Advanced Signal Generator """
    none = 0
    scope = 1
    aux = 2
    ext = 3
    soft = 4
    map = (none, scope, aux, ext, soft)
    labels = {none: "none", scope: "scope", aux: "aux in", ext: "ext in", soft: "software"}


class IndexModes(dict2class):
    """ Collection of Index Modes for AWG operation """
    single = 0
    dual = 1
    quad = 2
    map = (single, dual, quad)
    labels = {single: "single", dual: "dual", quad: "quad"}
    values = {single: 1, dual: 2, quad: 4}


class TriggerChannels(dict2class):
    """ Collection of channels used in triggering """
    A = Channels.A
    B = Channels.B
    C = Channels.C
    D = Channels.D
    Ext = 4
    Aux = 5
    map = (A, B, C, D, Ext, Aux)
    labels = {A: "A", B: "B", C: "C", D: "D", Ext: "EXT", Aux: "AUX"}


class ThresholdDirections(dict2class):
    """ Collection of Trigger Directions for Advanced Triggers """
    above = 0
    inside = above
    below = 1
    outside = below
    rising = 2
    enter = rising
    none = rising
    falling = 3
    exit = falling
    rising_or_falling = 4
    enter_or_exit = rising_or_falling
    above_lower = 5
    below_lower = 6
    rising_lower = 7
    falling_lower = 8
    positive_runt = 9
    negative_runt = 10
    map = (above, below, rising, falling,
           rising_or_falling, above_lower, below_lower, rising_lower, falling_lower, positive_runt, negative_runt)
    simple = (above, below, rising, falling)
    labels = {above: "above", below: "below", rising: "rising", falling: "falling", rising_or_falling: "rise/fall",
              above_lower: "above/low", below_lower: "below/low", rising_lower: "rise/low", falling_lower: "fall/low",
              positive_runt: "pos runt", negative_runt: "neg runt"}


class DigitalDirections(dict2class):
    """ Collection of Trigger Directions for Digital Triggers """
    dont_care = 0
    low = 1
    high = 2
    rising = 3
    falling = 4
    rising_or_falling = 5
    map = (dont_care, low, high, rising, falling, rising_or_falling)
    labels = {dont_care: "don't care", low: "low", high: "high",
              rising: "rising", falling: "falling", rising_or_falling: "rise/fall"}


class TriggerChannelDirections(dict2class):
    """ container for channel directions """

    def __init__(self, *args, **kwargs):
        for c in TriggerChannels.map:
            self.__dict__[TriggerChannels.labels[c]] = ThresholdDirections.none
            self.update(*args, **kwargs)


class TriggerState(dict2class):
    """ Collection of Trigger states for Advanced Triggers """
    dont_care = 0
    true = 1
    false = 2
    map = (dont_care, true, false)
    labels = {dont_care: "don't care", true: "true", false: "false"}


class TriggerConditionsStruct(Structure):
    """ CType specifier for Trigger Conditions """
    _fields_ = [
        ("chA", c_int32),
        ("chB", c_int32),
        ("chC", c_int32),
        ("chD", c_int32),
        ("ext", c_int32),
        ("aux", c_int32),
        ("pwq", c_int32),
        ("dig", c_int32),
    ]
    _pack_ = 1


class TriggerConditions(dict2class):
    """ Collection of Trigger Conditions for Advanced Triggering """
    chA = TriggerState.dont_care
    chB = TriggerState.dont_care
    chC = TriggerState.dont_care
    chD = TriggerState.dont_care
    ext = TriggerState.dont_care
    aux = TriggerState.dont_care
    pwq = TriggerState.dont_care
    dig = TriggerState.dont_care

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def to_struct(self):
        return TriggerConditionsStruct(self.chA, self.chB, self.chC, self.chD, self.ext, self.aux, self.pwq, self.dig)

    def is_set(self):
        return len([c for c in
                    (self.chA, self.chB, self.chC, self.chD, self.ext, self.aux, self.pwq, self.dig)
                    if c != TriggerState.dont_care]) > 0


class PwqConditionsStruct(Structure):
    """ CType specifier for Pulse Width Qualifier Conditions """
    _fields_ = [
        ("chA", c_int32),
        ("chB", c_int32),
        ("chC", c_int32),
        ("chD", c_int32),
        ("ext", c_int32),
        ("aux", c_int32),
        ("dig", c_int32),
    ]
    _pack_ = 1


class PwqConditions(dict2class):
    """ Collection of Pulse Width Qualifier Conditions """
    chA = TriggerState.dont_care
    chB = TriggerState.dont_care
    chC = TriggerState.dont_care
    chD = TriggerState.dont_care
    ext = TriggerState.dont_care
    aux = TriggerState.dont_care
    dig = TriggerState.dont_care

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def to_struct(self):
        return PwqConditionsStruct(self.chA, self.chB, self.chC, self.chD, self.ext, self.aux, self.dig)

    def is_set(self):
        return len([c for c in
                    (self.chA, self.chB, self.chC, self.chD, self.ext, self.aux, self.dig)
                    if c != TriggerState.dont_care]
                   ) > 0


class PwqTypes(dict2class):
    """ Collection of Pulse Width Qualifier types """
    none = 0
    less_than = 1
    lt = less_than
    greater_than = 2
    gt = greater_than
    in_range = 3
    inside = in_range
    out_of_range = 4
    outside = out_of_range
    map = (none, lt, gt, inside, outside)
    labels = {none: "None", lt: "Less Than", gt: "Greater Than", inside: "Inside", outside: "Outside"}


class DigitalChannelDirectionStruct(Structure):
    """ CType specifier for Digital triggers """
    _fields_ = [
        ("portbit", c_int32),
        ("direction", c_int32)
    ]
    _pack_ = 1


class TriggerChannelPropertiesStruct(Structure):
    """ CType specifier for Trigger Channel Properties in Advanced Triggers """
    _fields_ = [
        ("threshUpperADC", c_int16),
        ("threshUpperHys", c_uint16),
        ("threshLowerADC", c_int16),
        ("threshLowerHys", c_uint16),
        ("channel", c_int32),
        ("threshMode", c_int32)
    ]
    _pack_ = 1


class TriggerChannelProperties(dict2class):
    """ Object describing single Channel Trigger Properties in Advanced Triggers """
    threshUpperADC = 0.2
    threshUpperHys = 32767
    threshLowerADC = -32767
    threshLowerHys = 0
    threshMode = ThresholdModes.level
    direction = ThresholdDirections.none

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        self.update(self, *args, **kwargs)

    def to_struct(self):
        """ Translate object to ctypes structure
        :return: object
        """
        return TriggerChannelPropertiesStruct(self.threshUpperADC, self.threshUpperHys,
                                              self.threshLowerADC, self.threshLowerHys,
                                              self.channel, self.threshMode)


class ETSModes(dict2class):
    """ Collection of ETS modes """
    off = 0
    fast = 1
    slow = 2
    max = 3
    map = (off, fast, slow, max)
    labels = {off: "off", fast: "fast", slow: "slow", max: "max"}


class TimeUnits(dict2class):
    """ Collection of Time Units used in Timebase calculations """
    fs = 0
    ps = 1
    ns = 2
    us = 3
    ms = 4
    s = 5
    max = 6
    map = (fs, ps, ns, us, ms, s)
    labels = {fs: "fs", ps: "ps", ns: "ns", us: "μs", ms: "ms", s: "s"}
    ascii_labels = {fs: "fs", ps: "ps", ns: "ns", us: "us", ms: "ms", s: "s"}

    @staticmethod
    def nanofactors(unit):
        """ Returns power factor to bring interval value to nanoseconds """
        factor = -6
        for u in TimeUnits.map:
            if u != unit:
                factor += 3
            else:
                break
        return factor

    @staticmethod
    def secfactors(unit):
        """ Returns power factor to bring interval value to seconds """
        factor = 15
        for u in TimeUnits.map:
            if u != unit:
                factor -= 3
            else:
                break
        return factor

    @staticmethod
    def multiplier(f, t):
        """ Returns multiplier for bringing time value from one unit to another
        :param f: from units enum
        :type f: int
        :param t: to units enum
        :type t: int
        :return: multiplier
        :rtype : float
        """
        if f not in TimeUnits.map or t not in TimeUnits.map:
            return 0
        if f > t:
            return 1.0 * pow(10, (f - t) * 3)
        elif f < t:
            return 1.0 / pow(10, (t - f) * 3)
        else:
            return 1.0

ldlib = object()


class PS5000Device(object):
    def __init__(self, libobj):
        if not hasattr(self, "m"):
            self.m = sys.modules[__name__]
            raise NotImplementedError("Driver Module reference not set")
        self._handle = 0
        self._chandle = c_int16(0)
        self._channel_set = {}
        self._port_set = {}
        self.info = self.m.UnitInfo()
        self.trigger = False
        self.trigg_source = self.m.Channels.A
        self.trigg_threshold = 0.0
        self.trigg_direction = self.m.ThresholdDirections.rising
        self.trigg_ratio = 0.5
        self.trigg_wait = 0
        self.trigger_conditions = ()
        self.trigger_analog = ()
        self.trigger_digital = ()
        self.pwq_conditions = ()
        self.pwq_direction = self.m.ThresholdDirections.rising
        self.pwq_lower = 0
        self.pwq_upper = 0
        self.pwq_type = self.m.PwqTypes.none
        self._ets = dict2class()
        self._ets.mode = self.m.ETSModes.off
        self._ets.last = self.m.ETSModes.off
        self._ets.cycles = 0
        self._ets.interleaves = 0
        self._ets.picos = 0.0
        self._ets.status = pico_num("PICO_OK")
        self._ets.time = None
        self._segments = 0
        self._start_segment = None
        self._stop_segment = None
        self._bulk_indexes = ()
        self._collect_indexes = None
        self._collect_event = Event()
        if self._collect_event.is_set():
            self._collect_event.clear()
        self._collect_cb_type = None
        self._collect_cb_func = None
        self._tape = None
        self._records = None
        self._leavers = None
        self._recording_thread = None
        self._recording_lock = Lock()
        if self._recording_lock.acquire(False):
            self._recording_lock.release()
        self._recording_event = Event()
        if self._recording_event.is_set():
            self._recording_event.clear()
        self._async_lock = Lock()
        if self._async_lock.acquire(False):
            self._async_lock.release()
        self._async_event = Event()
        if self._async_event.is_set():
            self._async_event.clear()
        self._async_cb_type = None
        self._async_cb_func = None
        self._overlapped_samples = c_uint32(0)
        self._overlapped_ov = None
        self.last_error = None
        global ldlib
        ldlib = libobj

    def open_unit(self, serial=None):
        """ Opens unit
        :param serial: string specifying device serial and batch
        :type serial: string
        :returns: status of the call
        :rtype: int
        """
        """ Only one unit allowed per instance """
        if self._handle > 0:
            """ same will occur if 64 devices are opened... unlikely"""
            return pico_num("PICO_MAX_UNITS_OPENED")
        try:
            status = ldlib.OpenUnit(byref(self._chandle), c_char_p(serial))
        except AttributeError:
            return pico_num("PICO_NOT_FOUND")

        self._handle = self._chandle.value
        """ Read INFO from device, populate self.info """

        if status == pico_num("PICO_OK"):
            self.info.handle = self._handle
            status = self._set_info()
            if status == pico_num("PICO_OK"):
                """ Set device defaults """
                status = self.set_defaults()
        return status

    def _set_info(self):
        """ Pulls information from the driver to info class
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")

        for tag in ("DRIVER_VERSION", "USB_VERSION", "HARDWARE_VERSION",
                    "VARIANT_INFO", "BATCH_AND_SERIAL", "CAL_DATE",
                    "FIRMWARE_VERSION_1", "FIRMWARE_VERSION_2"):
            self.info[tag.lower()] = None
            line = create_string_buffer("\0", MAX_INFO_LEN)
            required = c_int16()
            if ("PICO_%s" % tag) in PICO_INFO:
                status = ldlib.GetUnitInfo(self._chandle, line, c_int16(MAX_INFO_LEN),
                                           byref(required), c_uint32(PICO_INFO["PICO_%s" % tag]))
                if status == pico_num("PICO_OK"):
                    self.info[tag.lower()] = line.value
        if self.info.variant_info is not None:
            status = self._set_variant_info()
        else:
            status = pico_num("PICO_INFO_UNAVAILABLE")
        if status == pico_num("PICO_OK"):
            status = self._set_memory_info()
        if status != pico_num("PICO_OK"):
            return status
        self.info.channel_ranges = dict2class()

        inner = False
        outer = False
        max_offset = c_float(0)
        min_offset = c_float(0)
        for i in self.m.Ranges.map:
            if not inner and i == self.info.min_range:
                inner = True
            if not outer and i > self.info.max_range:
                outer = True
            if not inner or outer:
                continue
            r = dict2class()
            r.label = self.m.Ranges.labels[i]
            r.value = self.m.Ranges.values[i]
            r.ascii_label = self.m.Ranges.ascii_labels[i]
            r.enum = i
            if hasattr(ldlib, "GetAnalogueOffset"):
                # dc
                status = ldlib.GetAnalogueOffset(self._chandle, r.enum, self.m.Couplings.dc,
                                                 byref(max_offset), byref(min_offset))
                if status == pico_num("PICO_OK"):
                    r.max_dc_offset = max_offset.value
                    r.min_dc_offset = min_offset.value
                else:
                    r.max_dc_offset = None
                    r.min_dc_offset = None
                # ac
                status = ldlib.GetAnalogueOffset(self._chandle, r.enum, self.m.Couplings.ac,
                                                 byref(max_offset), byref(min_offset))
                if status == pico_num("PICO_OK"):
                    r.max_ac_offset = max_offset.value
                    r.min_ac_offset = min_offset.value
                else:
                    r.max_ac_offset = None
                    r.min_ac_offset = None
            else:
                r.max_dc_offset = None
                r.min_dc_offset = None
                r.max_ac_offset = None
                r.min_ac_offset = None
            self.info.channel_ranges[i] = r
        if hasattr(ldlib, "MinimumValue") and hasattr(ldlib, "MaximumValue"):
            limit = c_int16(0)
            status = ldlib.MinimumValue(self._chandle, byref(limit))
            if status == pico_num("PICO_OK"):
                self.info.min_adc = limit.value
            else:
                self.info.min_adc = None
            status = ldlib.MaximumValue(self._chandle, byref(limit))
            if status == pico_num("PICO_OK"):
                self.info.max_adc = limit.value
            else:
                self.info.max_adc = None
        else:
            self.info.min_adc = -32512
            self.info.max_adc = 32512
        if hasattr(ldlib, "SigGenArbitraryMinMaxValues"):
            minv = c_int16(0)
            maxv = c_int16(0)
            mins = c_uint32(0)
            maxs = c_uint32(0)
            status = ldlib.SigGenArbitraryMinMaxValues(self._chandle,
                                                       byref(minv), byref(maxv), byref(mins), byref(maxs))
            if status == pico_num("PICO_OK"):
                self.info.awg_min = minv.value
                self.info.awg_max = maxv.value
                self.info.awg_size = maxs.value
        else:
            self.info.awg_min = -32767
            self.info.awg_max = 32768
        return pico_num("PICO_OK")

    def _set_memory_info(self):
        """ Sets initial memory setup
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        self._buffers = {}
        self._segments = 1
        mem = c_int32()
        status = self._memory_segments(self._segments, byref(mem))
        self.info.memory = mem.value
        self.info.memps = mem.value
        if status == pico_num("PICO_OK"):
            seg = c_uint32()
            status = ldlib.GetMaxSegments(self._chandle, byref(seg))
            self.info.max_segments = seg.value
        return status

    def _set_variant_info(self):
        """ Sets device variant specific properties
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if not hasattr(self.info, "variant_info") or self.info.variant_info is None:
            return pico_num("PICO_INFO_UNAVAILABLE")
        """ each subclass should have its own override """
        return pico_num("PICO_INFO_UNAVAILABLE")

    def set_defaults(self):
        """ Sets device into default state
        Each subclass should have its own implementation
        :returns: status of subsequent calls
        :rtype: int
        """
        return pico_num("PICO_INFO_UNAVAILABLE")

    def flash_led(self, count=1):
        """ Flashes device's LED count times
        :param count: number of flashes
        :type count: int
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        return ldlib.FlashLed(self._chandle, c_int16(count))

    def set_channel(self, channel, state):
        """ Sets device's selected channel into requested state
        :param channel: channel number as in Channels
        :type channel: int
        :param state: ChannelState object with desired setup
        :type state: ChannelState
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if not isinstance(state, self.m.ChannelState):
            return pico_num("PICO_INVALID_PARAMETER")
        status = ldlib.SetChannel(self._chandle, c_int32(channel), c_int16(state.enabled), c_int32(state.coupling),
                                  c_int32(state.range), c_float(state.offset))
        if status == pico_num("PICO_OK"):
            state.overvoltaged = False
            self._channel_set[channel] = deepcopy(state)
        return status

    def get_channel_state(self, channel):
        """ Returns current ChannelState object describing channel
        :param channel: channel number as in Channels
        :type channel: int
        :returns: state of the channel
        :rtype: ChannelState
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), None
        if channel not in self._channel_set.keys():
            return pico_num("PICO_INVALID_CHANNEL"), None
        return pico_num("PICO_OK"), deepcopy(self._channel_set[channel])

    def is_channel_overvoltaged(self, channel):
        """ Checks if channel is overvoltaged after latest collection
        Will return False when parameters check fails.
        :param channel: channel number as in Channels
        :type channel: int
        :returns: overvoltage check result
        :rtype: bool
        """
        if self._handle <= 0 or channel not in self._channel_set.keys():
            return False
        return self._channel_set[channel].overvoltaged

    def increase_channel_range(self, channel, step=1):
        """ Increase channel range setting by number of steps.
        If step <= 0 - set maximum available range
        :param channel: channel number as in Channels
        :type channel: int
        :param step: number of ranges to increase by
        :rtype step: int
        :returns: status of subsequent calls
        :rtype: int
        """
        status, state = self.get_channel_state(channel)
        if status != pico_num("PICO_OK"):
            return status
        if state is None:
            return pico_num("PICO_INVALID_STATE")
        if state.range == self.info.max_range:
            return pico_num("PICO_OK")
        if step <= 0:
            state.range = self.info.max_range
        else:
            for r in self.m.Ranges.map:
                if r > state.range:
                    step -= 1
                if step == 0 or r == self.info.max_range:
                    break
            else:
                r = None
            state.range = r
        return self.set_channel(channel, state)

    def decrease_channel_range(self, channel, step=1):
        """ Decrease channel range setting by number of steps.
        If step <= 0 - set minimum available range
        :param channel: channel number as in Channels
        :type channel: int
        :param step: number of ranges to decrease by
        :rtype step: int
        :returns: status of subsequent calls
        :rtype: int
        """
        status, state = self.get_channel_state(channel)
        if status != pico_num("PICO_OK"):
            return status
        if state is None:
            return pico_num("PICO_INVALID_STATE")
        if state.range == self.info.min_range:
            return pico_num("PICO_OK")
        if step <= 0:
            state.range = self.info.min_range
        else:
            rangelist = self.m.Ranges.map
            rangelist.reverse()
            for r in rangelist:
                if r < state.range:
                    step -= 1
                if step == 0 or r == self.info.min_range:
                    break
            else:
                r = None
            state.range = r

        return self.set_channel(channel, state)

    def set_digital_port(self, port, state):
        """ Sets properties of digital ports
        :param port: Port enum as in Ports
        :type port: int
        :param state: desired PortState of requested port
        :type state: PortState
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if self.info.num_ports == 0:
            return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")
        if not isinstance(state, self.m.PortState):
            return pico_num("PICO_INVALID_PARAMETER")
        adc_level = int(state.level / MAX_LOGIC_VOLTS * MAX_LOGIC_LEVEL)
        adc_level = MAX_LOGIC_LEVEL if adc_level > MAX_LOGIC_LEVEL \
            else MIN_LOGIC_LEVEL if adc_level < MIN_LOGIC_LEVEL \
            else adc_level
        status = ldlib.SetDigitalPort(self._chandle, c_int32(port), c_int16(state.enabled), c_int16(adc_level))
        if status == pico_num("PICO_OK"):
            self._port_set[port] = deepcopy(state)
        return status

    def get_digital_port_state(self, port):
        """ Returns current PortState object describing port
        :param port: portn enum as in Ports
        :type port: int
        :returns: state of the channel
        :rtype: PortState
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), None
        if self.info.num_ports == 0:
            return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE"), None
        if port not in self._port_set:
            return pico_num("PICO_INVALID_DIGITAL_PORT"), None
        return pico_num("PICO_OK"), deepcopy(self._port_set[port])

    def get_basic_interval(self, timebase):
        """ Return Device interval for given timebase
        :param timebase: timebase value
        :type timebase: int
        :returns: status of the calls, interval value
        :rtype: int, float
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), None
        interval = c_float()
        status = self._get_timebase(timebase=timebase, samples=1, ref_interval=byref(interval),
                                    oversample=0, ref_maxsamples=None, segment=0)
        return status, interval.value

    def _get_timebase(self, timebase, samples, ref_interval, oversample, ref_maxsamples, segment):
        return ldlib.GetTimebase(self._chandle, c_uint32(timebase), c_int32(samples), ref_interval, c_int16(oversample),
                                 ref_maxsamples, c_uint32(segment))

    def set_memory_segments(self, segments):
        """ Sets number of memory segments and returns number of available samples per segment
        Will release all allocated buffers.
        :param segments: number of segments to set up
        :type segments: int
        :returns status of the calls, number of available samples per segment
        :rtype: int, int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), 0
        """ Do not break data collection if its ongoing """
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                return pico_num("PICO_BUSY"), None
        if segments > self.info.max_segments:
            return pico_num("PICO_TOO_MANY_SEGMENTS"), 0
        if segments == 0:
            return pico_num("PICO_NOT_ENOUGH_SEGMENTS"), 0
        mem = c_int32()
        status = self._memory_segments(segments, byref(mem))
        if status == pico_num("PICO_OK"):
            self._segments = segments
            self.info.memps = mem.value
            return status, mem.value
        return status, 0

    def _memory_segments(self, segments, ref_mem):
        return ldlib.MemorySegments(self._chandle, c_uint32(segments), ref_mem)

    def locate_buffer(self, channel, samples, segment, mode, downsample, index=None):
        """ Locates/Creates internal buffer and returns stack index of it.
        :param channel: channel or port as in Channels or Ports
        :type channel: int
        :param samples: desired length of the buffer, after data reduction
        :type samples: int
        :param segment: corresponding memory segment number for the buffer
        :type segment: int
        :param mode: unmasked aka single data reduction mode as in RatioModes
        :type mode: int
        :param downsample: data reduction ratio
        :type downsample: int
        :param index: optional desired index number, if setting match existing - ignored
        :type index: int
        :returns: status of the calls, assigned index number
        :rtype: tuple(int, int)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), None
        """ validate channels """
        if channel not in (self._channel_set.keys() + self._port_set.keys()):
            if channel < self.m.Ports.p0:
                return pico_num("PICO_INVALID_CHANNEL"), None
            else:
                return pico_num("PICO_INVALID_DIGITAL_PORT"), None
        """ validate segments """
        if segment > self._segments:
            return pico_num("PICO_SEGMENT_OUT_OF_RANGE"), None
        """ validate mode """
        if not self.m.RatioModes.issingle(mode):
            return pico_num("PICO_RATIO_MODE_NOT_SUPPORTED"), None

        """ check if buffer of same spec / index exists """
        save_index = None
        if index is not None:
            if index in self._buffers:
                return self._reshape_buffer(index, channel, samples, segment, mode, downsample), index
            else:
                save_index = index
        """ check if buffer of given channel, segment and mode exists """
        for index in self._buffers.keys():
            if self._buffers[index].channel == channel \
                    and self._buffers[index].segment == segment and self._buffers[index].mode == mode:
                if save_index is not None:
                    self._buffers[save_index] = self._buffers.pop(index)
                    index = save_index
                return self._reshape_buffer(index, channel, samples, segment, mode, downsample), index
        """ allocate/recycle new index """
        if save_index is None:
            index = 0
            for i in self._buffers.keys():
                if i == index:
                    index += 1
                else:
                    break
        else:
            index = save_index
        """ allocate new buffer """
        self._buffers[index] = self.m.BufferInfo()
        with self._buffers[index].access_lock:
            self._buffers[index].inuse = Lock()
            self._buffers[index].data = None
            self._buffers[index].data_min = None
            self._buffers[index].channel = channel
            self._buffers[index].samples = samples
            self._buffers[index].segment = segment
            self._buffers[index].mode = mode
            self._buffers[index].downsample = downsample
            self._buffers[index].last_interval = None
            self._buffers[index].last_timebase = None
            self._buffers[index].real_interval = None
        return pico_num("PICO_OK"), index

    def locate_buffers(self, channel, samples, start_segment, stop_segment, mode, downsample):
        """ Locates/Creates internal buffers and returns stack index of it.
        :param channel: channel or port as in Channels or Ports
        :type channel: int
        :param samples: desired length of the buffer, after data reduction
        :type samples: int
        :param start_segment: memory segment number from
        :type start_segment: int
        :param stop_segment: memory segment number to
        :type stop_segment: int
        :param mode: unmasked aka single data reduction mode as in RatioModes
        :type mode: int
        :param downsample: data reduction ratio
        :type downsample: int
        :returns: status of the calls, assigned index numbers in the form of tuple
        :rtype: tuple(int, tuple())
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), ()
        if start_segment > self._segments or stop_segment >= self._segments:
            return pico_num("PICO_SEGMENT_OUT_OF_RANGE"), ()
        if start_segment > stop_segment:
            segments = range(start_segment, self._segments) + range(0, stop_segment + 1)
        else:
            segments = range(start_segment, stop_segment + 1)
        indexes = ()
        for segment in segments:
            status, number = self.locate_buffer(channel, samples, segment, mode, downsample)
            if status != pico_num("PICO_OK"):
                return status, indexes
            indexes += (number,)
        return pico_num("PICO_OK"), indexes

    def _reshape_buffer(self, index, channel, samples, segment, mode, downsample):
        """ Changes buffer properties to match specified """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if index not in self._buffers:
            return pico_num("PICO_INVALID_BUFFER")
        with self._buffers[index].access_lock:
            """ check if there is really anything to change """
            if self._buffers[index].channel == channel \
                    and self._buffers[index].samples == samples \
                    and self._buffers[index].segment == segment \
                    and self._buffers[index].mode == mode \
                    and (mode == self.m.RatioModes.none or self._buffers[index].downsample == downsample):
                return pico_num("PICO_OK")
            """ resize buffers if needed """
            if self._buffers[index].samples != samples:
                self._buffers[index].data = None
                self._buffers[index].data_min = None
            self._buffers[index].channel = channel
            self._buffers[index].samples = samples
            self._buffers[index].segment = segment
            self._buffers[index].mode = mode
            self._buffers[index].downsample = downsample
        return pico_num("PICO_OK")

    def _set_data_buffers(self, line, buffer_max, buffer_min, bufflen, segment, mode):
        return ldlib.SetDataBuffers(self._chandle, c_int32(line), buffer_max, buffer_min,
                                    c_int32(bufflen), c_uint32(segment), c_int32(mode))

    def _lock_buffer(self, index):
        """ Tries to acquire internal lock for the buffer """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if index not in self._buffers:
            return pico_num("PICO_INVALID_BUFFER")
        try:
            with self._buffers[index].access_lock:
                if not self._buffers[index].inuse.acquire(False):
                    return pico_num("PICO_BUSY")
        except:
            return pico_num("PICO_BUSY")
        return pico_num("PICO_OK")

    def unlock_buffer(self, index):
        """ Unlocks previously locked buffer
        :param index: buffer index number
        :type index: int
        :returns: status of the calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if index not in self._buffers:
            return pico_num("PICO_INVALID_BUFFER")
        try:
            with self._buffers[index].access_lock:
                self._buffers[index].inuse.release()
        except:
            return pico_num("PICO_OK")
        return pico_num("PICO_OK")

    def is_buffer_locked(self, index):
        """ Tests if given buffer is locked
        :param index: buffer index number
        :type index: int
        :returns: status of the calls
        :rtype: int
        """
        if self._handle <= 0 or index not in self._buffers:
            return False
        try:
            with self._buffers[index].access_lock:
                if self._buffers[index].inuse.acquire(False):
                    try:
                        self._buffers[index].inuse.release()
                    except:
                        return True
                else:
                    return True
        except:
            return False
        return False

    def unlock_all_buffers(self):
        """ Unlocks all currently allocated and locked buffers
        :returns: status of the calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if hasattr(self, "buffers"):
            for index in self._buffers.keys():
                self.unlock_buffer(index)

    def release_buffer(self, index):
        """ Removes buffer from requested index
        :param index: buffer index number
        :type index: int
        :returns: status of the calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if index not in self._buffers:
            return pico_num("PICO_INVALID_BUFFER")
        """ deallocate memory """
        self.unlock_buffer(index)
        with self._buffers[index].access_lock:
            a = self._buffers[index].access_lock
            self._buffers[index] = None
            self._buffers.pop(index)
        return pico_num("PICO_OK")

    def release_all_buffers(self):
        """ Removes all allocated buffers
        :returns: status of the calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if hasattr(self, "buffers"):
            for index in self._buffers.keys():
                self.release_buffer(index)
            self._buffers.clear()

    def get_buffer_info(self, index):
        """ Returns dictionary with buffer setup
        dict: {
            index,
            channel,
            samples,
            segment,
            mode,
            downsample,
            last_interval,
            last_timebase,
            real_interval
        }
        :param index: buffer index number
        :type index: int
        :returns: status of the calls
        :rtype: tuple(int, dict())
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), {}
        if index not in self._buffers:
            return pico_num("PICO_INVALID_BUFFER"), {}
        with self._buffers[index].access_lock:
            return pico_num("PICO_OK"), {
                "index": index,
                "channel": self._buffers[index].channel,
                "samples": self._buffers[index].samples,
                "segment": self._buffers[index].segment,
                "mode": self._buffers[index].mode,
                "downsample": self._buffers[index].downsample,
                "last_interval": self._buffers[index].last_interval,
                "last_timebase": self._buffers[index].last_timebase,
                "real_interval": self._buffers[index].real_interval
            }

    def get_buffer_data(self, index, unlock=True):
        """ Returns contents of the requested buffer in the form numpy array
        :param index: buffer index number
        :type index: int
        :param unlock: Whether to release buffer after the call
        :type unlock: bool
        :returns: status of the calls, data
        :rtype: tuple(int, np.array)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), []
        if index not in self._buffers.keys():
            return pico_num("PICO_INVALID_BUFFER"), []
        if unlock:
            self.unlock_buffer(index)
        with self._buffers[index].access_lock:
            return pico_num("PICO_OK"), self._buffers[index].data

    def get_buffer_volts(self, index, scale=1.0, unlock=True):
        """ Returns contents of the requested buffer in the form of numpy array
        Results can be scaled depending on value of scale parameter
        :param index: buffer index number
        :type index: int
        :param scale: scale of the data on return
        :type scale: float
        :param unlock: Whether to release buffer after the call
        :type unlock: bool
        :returns: status of the calls, data
        :rtype: tuple(int, np.array)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), []
        if index not in self._buffers.keys():
            return pico_num("PICO_INVALID_BUFFER"), []

        with self._buffers[index].access_lock:
            if self._buffers[index].data is None:
                return pico_num("PICO_INVALID_BUFFER"), []
        if unlock:
            self.unlock_buffer(index)
        with self._buffers[index].access_lock:
            factor = \
                scale * \
                (self.m.Ranges.values[self._channel_set[self._buffers[index].channel].range] / self.info.max_adc)
            return pico_num("PICO_OK"), self._buffers[index].data * factor

    def get_buffer_states(self, index, unlock=True):
        """ Returns contents of the requested buffer in the form of multidimensional numpy array
        :param index: buffer index number
        :type index: int
        :param unlock: Whether to release buffer after the call
        :type unlock: bool
        :returns: status of the calls, data
        :rtype: tuple(int, np.ndarray)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), []
        if index not in self._buffers.keys():
            return pico_num("PICO_INVALID_BUFFER"), []
        with self._buffers[index].access_lock:
            if self._buffers[index].data is None:
                return pico_num("PICO_INVALID_BUFFER"), []
        if unlock:
            self.unlock_buffer(index)
        with self._buffers[index].access_lock:
            return pico_num("PICO_OK"), np.array(
                [self._buffers[index].data & (1 << b) for b in range(0, 8)], dtype=bool)

    def get_min_max_data(self, index, unlock=True):
        """ Returns contents of the requested buffer in the form of 2 np.arrays
        This call applies only to aggregated mode
        :param index: buffer index number
        :type index: int
        :param unlock: Whether to release buffer after the call
        :type unlock: bool
        :returns: status of the calls, data_min, data_max
        :rtype: tuple(int, np.array, np.array)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), [], []
        if index not in self._buffers.keys():
            return pico_num("PICO_INVALID_BUFFER"), [], []
        if unlock:
            self.unlock_buffer(index)
        with self._buffers[index].access_lock:
            if self._buffers[index].data_min is not None:
                return pico_num("PICO_OK"), self._buffers[index].data_min, self._buffers[index].data
            else:
                return pico_num("PICO_OK"), self._buffers[index].data, self._buffers[index].data

    def get_min_max_volts(self, index, scale=1.0, unlock=True):
        """ Returns contents of the requested buffer in the form of 2 np.arrays
        This call applies only to aggregated mode
        :param index: buffer index number
        :type index: int
        :param scale: scale of the data on return
        :type scale: float
        :param unlock: Whether to release buffer after the call
        :type unlock: bool
        :returns: status of the calls, data_min, data_max
        :rtype: tuple(int, np.array, np.array)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), [], []
        if index not in self._buffers.keys():
            return pico_num("PICO_INVALID_BUFFER"), [], []
        with self._buffers[index].access_lock:
            if self._buffers[index].data is None:
                return pico_num("PICO_OK"), [], []
        if unlock:
            self.unlock_buffer(index)
        with self._buffers[index].access_lock:
            factor = \
                scale * \
                (self.m.Ranges.values[self._channel_set[self._buffers[index].channel].range] / self.info.max_adc)

            if self._buffers[index].data_min is not None:
                return pico_num("PICO_OK"), \
                       self._buffers[index].data_min * factor, self._buffers[index].data * factor
            else:
                a = self._buffers[index].data * factor
                return pico_num("PICO_OK"), a, a

    def get_min_max_states(self, index, unlock=True):
        """ Returns contents of the requested buffer in the form of 2 multidimensional np.arrays
        This call applies only to aggregated mode
        :param index: buffer index number
        :type index: int
        :param unlock: Whether to release buffer after the call
        :type unlock: bool
        :returns: status of the calls, data_min, data_max
        :rtype: tuple(int, np.ndarray, np.ndarray)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), [], []
        if index not in self._buffers.keys():
            return pico_num("PICO_INVALID_BUFFER"), [], []
        if unlock:
            self.unlock_buffer(index)
        with self._buffers[index].access_lock:
            if self._buffers[index].data is None:
                return pico_num("PICO_OK"), [], []
            if self._buffers[index].data_min is not None:
                return pico_num("PICO_OK"), np.array(
                    [self._buffers[index].data_min & (1 << b) for b in range(0, 8)], dtype=bool), np.array(
                    [self._buffers[index].data & (1 << b) for b in range(0, 8)], dtype=bool)
            else:
                a = np.array([self._buffers[index].data & (1 << b) for b in range(0, 8)], dtype=bool)
                return pico_num("PICO_OK"), a, a

    def get_ets_data(self, index, unlock=True):
        """ Returns contents of the requested buffer in the form of 2 numpy arrays: times, data
        :param index: buffer index number
        :type index: int
        :param unlock: Whether to release buffer after the call
        :type unlock: bool
        :returns: status of the calls, times, data_max
        :rtype: tuple(int, np.array, np.array)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), [], []
        if index not in self._buffers.keys() or self._ets.time is None:
            return pico_num("PICO_INVALID_BUFFER"), [], []
        if unlock:
            self.unlock_buffer(index)
        return pico_num("PICO_OK"), self._ets.time, self._buffers[index].data

    def collect_segment(self, segment,
                        interval=None, event_handle=None, timebase=None, block=True, bulk=False, overlapped=False):
        """ Runs Block data collection on(from) given segment.
        Can explicitly use supplied timebase if given or calculate one.
        Buffers have to be set at least on one channel to make this call work.
        :param segment: memory segment number to start the collection on (from)
        :type segment: int
        :param interval: sample interval in nanoseconds
        :type interval: float
        :param event_handle: event handle to use during the collection, once device is ready, it is set
        :type event_handle: Event
        :param timebase: explicit (forced) timebase value
        :type timebase: int
        :param block: whether to block the call, requires event_handle if False
        :type block: bool
        :param bulk: collect segments in bulk, better use collect_segments call
        :type bulk: bool
        :param overlapped: use overlapped buffer in collection
        :type overlapped: bool
        :returns: status of the call
        :rtype int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if segment > self._segments:
            return pico_num("PICO_SEGMENT_OUT_OF_RANGE")
        """ We expect only one collection at the time """
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                return pico_num("PICO_BUSY")
        """ Locate buffers taking part in collection """
        if bulk:
            if self._bulk_indexes is None or len(self._bulk_indexes) == 0:
                return pico_num("PICO_INVALID_BUFFER")
            indexes = self._bulk_indexes
        else:
            indexes = ()
            for index in self._buffers.keys():
                if self._buffers[index].segment == segment:
                    indexes += (index,)
            if len(indexes) == 0:
                return pico_num("PICO_INVALID_BUFFER")
        """ pick the longest sample number from defined buffers """
        samples = 0
        for index in indexes:
            with self._buffers[index].access_lock:
                if self._buffers[index].segment == segment:
                    if self._buffers[index].mode == self.m.RatioModes.none:
                        samples = max(samples, self._buffers[index].samples)
                    else:
                        samples = max(samples, self._buffers[index].samples * self._buffers[index].downsample)
                    break
        if samples == 0:
            return pico_num("PICO_INVALID_BUFFER")
        """ ets setup """
        if self._ets.mode != self._ets.last:
            if self._ets.mode == self.m.ETSModes.off:
                self._ets.status = ldlib.SetEts(self._chandle, c_int32(self.m.ETSModes.off),
                                                c_int16(self._ets.cycles), c_int16(self._ets.interleaves), None)
                if self._ets.status == pico_num("PICO_OK"):
                    self._ets.last = self.m.ETSModes.off
            elif (self.trigger or True in [c.is_set() for c in (self.trigger_conditions + self.pwq_conditions)]) \
                    and len([1 for p in self._port_set.keys() if self._port_set[p].enabled]) == 0:
                picos = c_int32(0)
                self._ets.status = ldlib.SetEts(self._chandle, c_int32(self._ets.mode), c_int16(self._ets.cycles),
                                                c_int16(self._ets.interleaves), byref(picos))
                if self._ets.status == pico_num("PICO_OK"):
                    self._ets.last = self._ets.mode
                    self._ets.picos = picos.value

        """ calculate timebase from interval """
        finterval = c_float(0.0)
        linterval = c_float(0.0)

        if self._ets.last != self.m.ETSModes.off and self._ets.status == pico_num("PICO_OK"):
            timebase = 1
            finterval.value = interval = float(picos.value) / 1000.0

        if isinstance(interval, (int, long)):
            interval = float(interval)

        if timebase is not None and self._ets.last == self.m.ETSModes.off:
            status = self._get_timebase(timebase=timebase, samples=samples, ref_interval=byref(finterval),
                                        oversample=0, ref_maxsamples=None, segment=segment)
            if status != pico_num("PICO_OK"):
                return status

        if timebase is None:
            for index in indexes:
                with self._buffers[index].access_lock:
                    if self._buffers[index].last_interval is not None \
                            and self._buffers[index].last_timebase is not None:
                        if self._buffers[index].last_interval == interval:
                            timebase = self._buffers[index].last_timebase
                            finterval.value = self._buffers[index].real_interval
                        break

        if timebase is None:
            last = 0
            status = pico_num("PICO_OK")
            for pwr in range(0, 32):
                rough = 1 << pwr
                status = self._get_timebase(timebase=rough, samples=samples, ref_interval=byref(finterval),
                                            oversample=0, ref_maxsamples=None, segment=segment)
                if status not in (pico_num("PICO_OK"), pico_num("PICO_INVALID_TIMEBASE")) \
                        or finterval.value >= interval:
                    break
                last = rough
            else:
                rough = last
            if status == pico_num("PICO_TOO_MANY_SAMPLES"):
                return status
            if last == rough or finterval.value == interval:
                timebase = rough
            else:
                if last <= 32:
                    fine = rough
                    for fine in range(int(last / 2), 64):
                        status = self._get_timebase(timebase=fine, samples=samples, ref_interval=byref(finterval),
                                                    oversample=0, ref_maxsamples=None, segment=segment)
                        if status == pico_num("PICO_OK") and finterval.value >= interval:
                            break
                        linterval.value = finterval.value
                    if abs(interval - finterval.value) <= abs(interval - linterval.value):
                        timebase = fine
                    else:
                        timebase = max(1, fine - 1)
                        finterval.value = linterval.value if linterval.value > 0 else interval
                else:
                    """ bubble :) """
                    i = 1
                    linterval.value = finterval.value
                    fine = rough
                    while timebase is None:
                        if i >= 32:
                            timebase = fine
                            break
                        elif linterval.value > interval:
                            fine -= int((rough - last) / pow(2, i))
                        elif linterval.value < interval:
                            fine += int((rough - last) / pow(2, i))
                        else:
                            timebase = fine
                            continue

                        status = self._get_timebase(timebase=fine, samples=samples, ref_interval=byref(finterval),
                                                    oversample=0, ref_maxsamples=None, segment=segment)
                        if status == pico_num("PICO_OK") and finterval.value in (interval, linterval.value):
                            timebase = fine
                            continue
                        linterval.value = finterval.value
                        i += 1
        else:
            pass
        if not bulk:
            self._lock_buffer(index)
        for index in indexes:
            with self._buffers[index].access_lock:
                self._buffers[index].last_interval = interval
                self._buffers[index].last_timebase = timebase
                self._buffers[index].real_interval = finterval.value

        """ setup callback """
        self._collect_cb_type = self._block_ready()
        self._collect_cb_func = self._collect_cb_type(self._collect_cb)
        self._collect_indexes = indexes
        if event_handle is not None:
            self._collect_event = event_handle
        self._collect_event.clear()

        if self.trigger or True in [c.is_set() for c in (self.trigger_conditions + self.pwq_conditions)]:
            pretrig = int(samples * self.trigg_ratio)
            posttrig = samples - pretrig
        else:
            pretrig = 0
            posttrig = samples
        if overlapped:
            status = self.set_overlapped_buffers(self._collect_indexes)
            if status != pico_num("PICO_OK"):
                return status
        """ run block collection """
        try:
            status = self._run_block(pretrig=pretrig, posttrig=posttrig, timebase=timebase, oversample=0, ref_time=None,
                                     segment=segment, ref_cb=self._collect_cb_func, ref_cb_param=None)
        except Exception as ex:
            print "Run Block(%d):" % sys.exc_info()[-1].tb_lineno, ex.message, type(ex)
            self.stop()
            status = pico_num("PICO_OPERATION_FAILED")
        if status != pico_num("PICO_OK"):
            return status
        if block:
            self._collect_event.wait()
            if not overlapped:
                if bulk:
                    status = self._get_buffer_values_bulk(self._collect_indexes)
                else:
                    status = self._get_buffer_values(self._collect_indexes)
            else:
                if bulk:
                    pass
                else:
                    for c in self._channel_set.keys():
                        self._channel_set[c].overvoltaged = self._overlapped_ov.value & (1 << c) != 0
            self._collect_event.clear()
            return status
        else:
            return pico_num("PICO_OK")

    def _run_block(self, pretrig, posttrig, timebase, oversample, ref_time, segment, ref_cb, ref_cb_param):
        return ldlib.RunBlock(self._chandle, c_int32(pretrig), c_int32(posttrig), c_uint32(timebase),
                              c_int16(oversample), ref_time, c_uint32(segment), ref_cb, ref_cb_param)

    def collect_segment_overlapped(self, segment, interval=None, event_handle=None, timebase=None, block=True):
        """ Runs Block data collection on(from) given segment in overlapped setup.
        Can explicitly use supplied timebase if given or calculate one.
        Buffers have to be set at least on one channel to make this call work.
        :param segment: memory segment number to start the collection on (from)
        :type segment: int
        :param interval: sample interval in nanoseconds
        :type interval: float
        :param event_handle: event handle to use during the collection, once device is ready, it is set
        :type event_handle: Event
        :param timebase: explicit (forced) timebase value
        :type timebase: int
        :param block: whether to block the call, requires event_handle if False
        :type block: bool
        :param bulk: collect segments in bulk, better use collect_segments call
        :type bulk: bool
        :param overlapped: use overlapped buffer in collection
        :type overlapped: bool
        :returns: status of the call
        :rtype int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        return self.collect_segment(segment=segment, interval=interval, event_handle=event_handle, timebase=timebase,
                                    block=block, overlapped=True)

    def _collect_cb(self, *args):
        """ Callback function for collect segment run block """
        try:
            if self._collect_event is not None:
                self._collect_event.set()
        except:
            return

    def collect_segments(self, start_segment, stop_segment, interval=None, event_handle=None, timebase=None,
                         block=True):
        """ Initiates Rapid Block Collection
        :param start_segment: number of segment to start the collection from
        :type start_segment: int
        :param stop_segment: number of last segment to be collected
        :type stop_segment: int
        :param interval: nanoseconds per sample, optional if timebase specified
        :type interval: int
        :param event_handle: reference to the event object to notify about completion
        :type event_handle: threading._Event
        :param timebase: optional timebase to skip internal calculation from interval
        :type timebase: int
        :return: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if start_segment >= self._segments or stop_segment >= self._segments:
            return pico_num("PICO_SEGMENT_OUT_OF_RANGE")
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                return pico_num("PICO_BUSY")

        number = stop_segment - start_segment + 1 if stop_segment >= start_segment \
            else self._segments - start_segment + stop_segment + 1
        status = self._set_no_of_captures(number=number)
        if status != pico_num("PICO_OK"):
            return status
        segs = (start_segment,) if start_segment == stop_segment \
            else range(start_segment, stop_segment + 1) if stop_segment > start_segment \
            else range(start_segment, self._segments) + range(0, stop_segment + 1)
        self._bulk_indexes = ()
        for index in self._buffers.keys():
            with self._buffers[index].access_lock:
                if self._buffers[index].segment in segs:
                    self._bulk_indexes += (index,)
        self._start_segment = start_segment
        self._stop_segment = stop_segment
        status = self.collect_segment(start_segment, interval=interval, event_handle=event_handle,
                                      timebase=timebase, bulk=True, block=block)
        self._start_segment = None
        self._stop_segment = None
        for index in self._buffers.keys():
            with self._buffers[index].access_lock:
                if self._buffers[index].segment == start_segment:
                    interval = self._buffers[index].last_interval
                    timebase = self._buffers[index].last_timebase
                    real_int = self._buffers[index].real_interval
                    break
        else:
            interval = 0
            timebase = 0
            real_int = 0

        for index in self._buffers.keys():
            with self._buffers[index].access_lock:
                if self._buffers[index].segment in segs:
                    self._buffers[index].last_interval = interval
                    self._buffers[index].last_timebase = timebase
                    self._buffers[index].real_interval = real_int
            self._lock_buffer(index)
        return status

    def set_overlapped_buffers(self, indexes):
        """ Preallocate collection buffers in overlapped mode
        :param indexes: list of buffer indexes to preallocate
        :type indexes: list, tuple
        :return: status of the calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if len(indexes) == 0:
            return pico_num("PICO_INVALID_BUFFER")
        """ get values into buffers """
        self._overlapped_samples.value = 0
        status = pico_num("PICO_OK")
        segs = ()
        ds = None
        mode = 0
        for index in indexes:
            with self._buffers[index].access_lock:
                if index not in self._buffers.keys():
                    return pico_num("PICO_INVALID_BUFFER")
                self._buffers[index].nanooffset = 0
                if self._buffers[index].samples > self._overlapped_samples.value:
                    self._overlapped_samples.value = self._buffers[index].samples
                if self._buffers[index].segment not in segs:
                    segs += (self._buffers[index].segment,)
                if ds is None:
                    ds = self._buffers[index].downsample
                elif ds != self._buffers[index].downsample:
                    return pico_num("PICO_INVALID_BUFFER")
                mode |= self._buffers[index].mode

        self._overlapped_samples.value *= ds
        if len(segs) == 0:
            return pico_num("PICO_INVALID_BUFFER")
        elif len(segs) > 1:
            self._overlapped_ov = np.zeros(shape=(len(segs), ), dtype=c_uint32)
            status = ldlib.GetValuesOverlappedBulk(self._chandle, c_uint32(0), byref(self._overlapped_samples),
                                                   c_uint32(ds), c_int32(mode), c_uint32(min(segs)),
                                                   c_uint32(max(segs)), self._overlapped_ov.ctypes)
        else:
            self._overlapped_ov = c_uint32(0)
            status = ldlib.GetValuesOverlapped(self._chandle, c_uint32(0), byref(self._overlapped_samples),
                                               c_uint32(ds), c_int32(mode), c_uint32(segs[0]),
                                               byref(self._overlapped_ov))
        if status != pico_num("PICO_OK"):
            return status

        """ set buffer on the driver """
        for index in indexes:
            with self._buffers[index].access_lock:
                if self._buffers[index].data is None or len(self._buffers[index].data) != self._buffers[index].samples:
                    self._buffers[index].data = np.empty(self._buffers[index].samples, c_int16)
                if self._buffers[index].mode == self.m.RatioModes.agg:
                    if self._buffers[index].data_min is None \
                            or len(self._buffers[index].data_min) != self._buffers[index].samples:
                        self._buffers[index].data_min = np.empty(self._buffers[index].samples, c_int16)
        status = self._setbuffers(indexes)
        return status

    def _set_no_of_captures(self, number):
        return ldlib.SetNoOfCaptures(self._chandle, c_uint32(number))

    def _get_buffer_values(self, indexes):
        """ Pulls values from the driver to the buffer of requested indexes
        :param indexes: list of index of buffers to fill them with data
        :type indexes: tuple
        :return: picostatus number of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        """ get values into buffers """
        status = pico_num("PICO_OK")
        segment = None
        modes = {}
        max_samples = 0
        for index in indexes:
            with self._buffers[index].access_lock:
                if index not in self._buffers.keys():
                    return pico_num("PICO_INVALID_BUFFER")
                if segment is None:
                    segment = self._buffers[index].segment
                elif segment != self._buffers[index].segment:
                    return pico_num("PICO_TOO_MANY_SEGMENTS")
                self._buffers[index].nanooffset = 0
                bufflen = self._buffers[index].samples
                if bufflen > max_samples:
                    max_samples = bufflen
                """ set buffer on the driver """
                if self._buffers[index].data is None or len(self._buffers[index].data) != bufflen:
                    self._buffers[index].data = np.empty(bufflen, c_int16)
                if self._buffers[index].mode == self.m.RatioModes.agg:
                    if self._buffers[index].data_min is None or len(self._buffers[index].data_min) != bufflen:
                        self._buffers[index].data_min = np.empty(bufflen, c_int16)
                if self._buffers[index].mode not in modes.keys():
                    modes[self._buffers[index].mode] = self._buffers[index].downsample
            status = self._setbuffer(index)
            if status != pico_num("PICO_OK"):
                continue
        if self._ets.mode != self.m.ETSModes.off and self._ets.mode == self._ets.last:
            if self._ets.time is None or len(self._ets.time) != max_samples:
                self._ets.time = np.empty(max_samples, c_int64)
            status = ldlib.SetEtsTimeBuffer(self._chandle, self._ets.time.ctypes, max_samples)
        else:
            self._ets.time = None
            """ copy data """
        overvoltaged = c_int16(0)
        for mode in modes.keys():
            samples = c_uint32(max_samples * (modes[mode] if modes[mode] else 1))
            self._get_values(start=0, ref_samples=byref(samples), ratio=modes[mode], mode=mode,
                             segment=segment, ref_overflow=byref(overvoltaged))
            status = ldlib.SetEtsTimeBuffer(self._chandle, None, samples.value)
        """ tell driver to release buffers """
        status = self._setbuffers(indexes, False)
        """ check for overvoltage """
        if overvoltaged.value != 0:
            for c in self._channel_set.keys():
                self._channel_set[c].overvoltaged = overvoltaged.value & (1 << c) != 0
        return status

    def _get_values(self, start, ref_samples, ratio, mode, segment, ref_overflow):
        return ldlib.GetValues(self._chandle, c_uint32(start), ref_samples,
                               c_uint32(ratio), c_int32(mode), c_uint32(segment), ref_overflow)

    def _get_buffer_values_bulk(self, indexes):
        """ Pulls values from the driver to the buffer of requested indexes - in one bulk
        :param indexes: list of index of buffers to fill them with data
        :type indexes: tuple
        :return: picostatus number of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if self._start_segment is None or self._stop_segment is None:
            return pico_num("PICO_INVALID_BUFFER")
        """ organise time offsets """
        nanooffsets = {}
        length = self._stop_segment - self._start_segment + 1 if self._stop_segment >= self._start_segment \
            else self._segments - self._start_segment + self._stop_segment + 1
        offsets = np.zeros(length, dtype=c_int64)
        units = np.zeros(length, dtype=c_int32)
        status = self._get_values_trigger_time_offset_bulk(ref_offsets=offsets.ctypes, ref_units=units.ctypes,
                                                           start_segment=self._start_segment,
                                                           stop_segment=self._stop_segment)
        if status != pico_num("PICO_OK"):
            return status
        segment = self._start_segment
        for i in range(0, length):
            nanooffsets[segment] = offsets[i] * (10 ** self.m.TimeUnits.nanofactors(units[i]))
            segment += 1
            if segment >= self._segments:
                segment = 0
        """ get values into buffers """
        samples = c_uint32()
        mode = self.m.RatioModes.none
        if len(indexes) > 0:
            with self._buffers[indexes[0]].access_lock:
                samples.value = self._buffers[indexes[0]].samples
                ratio = self._buffers[indexes[0]].downsample
        else:
            return pico_num("PICO_NO_SAMPLES_AVAILABLE")
        for index in indexes:
            with self._buffers[index].access_lock:
                if self._buffers[index].samples != samples.value or self._buffers[index].downsample != ratio:
                    return pico_num("PICO_INVALID_BUFFER")
                self._buffers[index].nanooffset = nanooffsets[self._buffers[index].segment]
                """ set buffer on the driver """
                if self._buffers[index].data is None or len(self._buffers[index].data) != samples.value:
                    self._buffers[index].data = np.empty(samples.value, c_int16)
                if self._buffers[index].mode == self.m.RatioModes.agg:
                    if self._buffers[index].data_min is None or len(self._buffers[index].data_min) != samples.value:
                        self._buffers[index].data_min = np.empty(samples.value, c_int16)
                mode |= self._buffers[index].mode
        status = self._setbuffers(indexes)
        if status != pico_num("PICO_OK"):
            return status
        overvoltaged = np.zeros(length, dtype=c_int16)
        status = self._get_values_bulk(ref_samples=byref(samples), start_segment=self._start_segment,
                                       stop_segment=self._stop_segment, ratio=ratio, mode=mode,
                                       ref_overflow=overvoltaged.ctypes)
        if status != pico_num("PICO_OK"):
            return status
        """ check for overvoltage """
        for c in self._channel_set.keys():
            bit = 1 << c
            self._channel_set[c].overvoltaged = bit in (overvoltaged & bit)
        """ tell driver to release buffers """
        status = self._setbuffers(indexes, False)
        return status

    def _setbuffer(self, index, enable=True):
        return self._setbuffers(indexes=(index,), enable=enable)

    def _setbuffers(self, indexes, enable=True):
        for index in indexes:
            with self._buffers[index].access_lock:
                status = \
                    self._set_data_buffers(line=self._buffers[index].channel,
                                           buffer_max=self._buffers[index].data.ctypes if enable else None,
                                           buffer_min=(self._buffers[index].data_min.ctypes
                                                       if enable and self._buffers[index].mode == self.m.RatioModes.agg
                                                       else None),
                                           bufflen=self._buffers[index].samples,
                                           segment=self._buffers[index].segment, mode=self._buffers[index].mode)
            if status != pico_num("PICO_OK"):
                return status
        return pico_num("PICO_OK")

    def _get_values_trigger_time_offset_bulk(self, ref_offsets, ref_units, start_segment, stop_segment):
        return ldlib.GetValuesTriggerTimeOffsetBulk(self._chandle, ref_offsets, ref_units,
                                                    c_uint32(start_segment), c_uint32(stop_segment))

    def _get_values_bulk(self, ref_samples, start_segment, stop_segment, ratio, mode, ref_overflow):
        return ldlib.GetValuesBulk(self._chandle, ref_samples, c_uint32(start_segment), c_uint32(stop_segment),
                                   c_uint32(ratio), c_int32(mode), ref_overflow)

    def load_tape(self, tape):
        """ Loads/sets which streaming tape to use
        :param tape: tape object
        :type tape: StreamingTape
        :returns: status of the call
        :rtype int
        """
        if self._tape is not None:
            self.eject_tape()
        if isinstance(tape, StreamingTape):
            self._tape = tape
            return pico_num("PICO_OK")
        else:
            return pico_num("PICO_INVALID_PARAMETER")

    def eject_tape(self):
        """ Removes tape reference and prunes recording buffers
        :returns: PICO_OK
        :rtype: int
        """
        if self._tape is not None:
            self._tape = None
        self._records = None
        self._leavers = None
        return pico_num("PICO_OK")

    def start_recording(self, interval, units, mode, downsample=1, memlength=0, limit=0, chapter=None):
        """ Initiates Stream recording to the tape with requested sampling interval
        :param interval: interval per collected raw sample
        :type interval: int
        :param units: interval units, from TimeUnits
        :type units: int
        :param mode: data reduction mode, from RatioModes
        :type mode: int
        :param downsample: data reduction ratio
        :type downsample: int
        :param memlength: number of raw samples in memory buffers
        :type memlength: int
        :param limit: number of samples at which device will issue autostop, 0 to stream until stopped.
                      Required for horizontal trigger ratio in streaming to work.
        :type limit: int
        :param chapter: Chapter name for the records
        :type chapter: string, None
        :rtype: int
        :returns: status of the call
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if units not in self.m.TimeUnits.map:
            return pico_num("PICO_INVALID_TIMEBASE")
        if self._tape is None:
            return pico_num("PICO_BUFFERS_NOT_SET")
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                return pico_num("PICO_BUSY")
        if downsample == 0:
            return pico_num("PICO_INVALID_PARAMETER")

        with self._recording_lock:
            """ Gather how many channels/ports are enabled/engaged """
            enabled = len([1 for c in self._channel_set.keys() if self._channel_set[c].enabled])
            engaged = len([1 for p in self._port_set.keys() if self._port_set[p].enabled])
            """ none of the channels/ports are enabled """
            if enabled + engaged == 0:
                if enabled == 0:
                    return pico_num("PICO_INVALID_CHANNEL")
                if engaged == 0:
                    return pico_num("PICO_INVALID_DIGITAL_PORT")
            """ initialize records """
            self._records = StreamingTapeRecording()
            self._leavers = None
            self._records.device = self.info.variant_info
            self._records.serial = self.info.batch_and_serial
            """ Determine how many ratio modes to set up """
            self._records.modes = self.m.RatioModes.mode2dict(mode)
            # overview buff len
            if memlength == 0:
                if limit == 0:
                    # half a second of data
                    desired = \
                        int(interval * float(pow(10, self.m.TimeUnits.secfactors(units))) *
                            ceil((enabled + engaged) / 2.0))
                    bufflen = min(desired, STREAM_LENGTH)
                else:
                    bufflen = limit
            else:
                bufflen = memlength
            if limit == 0:
                samples = bufflen * downsample
            else:
                samples = limit * downsample
            if bufflen > samples:
                bufflen = samples
            if chapter is None:
                self._records.chapter = self._make_chapter_tag()
            else:
                self._records.chapter = chapter
            self._records.enabled = enabled + engaged
            self._records.units = units
            self._records.mode = mode
            self._records.downsample = downsample
            self._records.bufflen = bufflen
            self._records.max_samples = samples
            self._records.buffers = {}
            if limit > 0:
                self._records.final = False
            triggadv = (True in [c.is_set() for c in self.trigger_conditions])
            triggpwq = (True in [c.is_set() for c in self.pwq_conditions])
            if self.trigger or triggadv or triggpwq:
                self._records.triggerSet = True
                self._records.triggered = False
                pretrigger = min(samples, int(samples * self.trigg_ratio))
                postrigger = samples - pretrigger
                if self.trigger:
                    self._records.triggerSource = self.trigg_source
                    self._records.triggerThreshold = self.trigg_threshold
                    self._records.triggerDirection = self.trigg_direction
                if triggadv:
                    self._records.triggerConditions = self.trigger_conditions
                    self._records.triggerAnalog = self.trigger_analog
                    self._records.triggerDigital = self.trigger_digital
                if triggpwq:
                    self._records.pwqConditions = self.pwq_conditions
                    self._records.pwqDirection = self.pwq_direction
                    self._records.pwqLower = self.pwq_lower
                    self._records.pwqUpper = self.pwq_upper
                    self._records.pwqType = self.pwq_type
            else:
                self._records.triggerSet = False
                pretrigger = 0
                postrigger = samples
            lines = ()
            for chann in [c for c in self._channel_set.keys() if self._channel_set[c].enabled]:
                self._records.buffers[chann] = {}
                self._records.buffers[chann]["range"] = self._channel_set[chann].range
                self._records.buffers[chann]["scale"] = self.m.Ranges.values[self._channel_set[chann].range]
                lines += (chann,)
            for port in [p for p in self._port_set.keys() if self._port_set[p].enabled]:
                self._records.buffers[port] = {}
                self._records.buffers[port]["level"] = self._port_set[port].level
                lines += (port,)
            """ forcibly create raw buffer, if single """
            for line in lines:
                status = pico_num("PICO_OK")
                if self._records.mode == self.m.RatioModes.raw:
                    self._records.buffers[line]["raw"] = np.empty(shape=(self._records.bufflen,), dtype=c_int16)
                    status = self._set_data_buffers(line=line, buffer_max=self._records.buffers[line]["raw"].ctypes,
                                                    buffer_min=None, bufflen=self._records.bufflen, segment=0,
                                                    mode=self.m.RatioModes.raw)
                else:
                    for m in self._records.modes:
                        if self._records.modes[m] == self.m.RatioModes.agg:
                            self._records.buffers[line]["min"] = np.empty(shape=(self._records.bufflen,), dtype=c_int16)
                            self._records.buffers[line]["max"] = np.empty(shape=(self._records.bufflen,), dtype=c_int16)
                            status = self._set_data_buffers(line=line,
                                                            buffer_max=self._records.buffers[line]["max"].ctypes,
                                                            buffer_min=self._records.buffers[line]["min"].ctypes,
                                                            bufflen=self._records.bufflen, segment=0,
                                                            mode=self.m.RatioModes.agg)
                        else:
                            self._records.buffers[line][m] = np.empty(shape=(self._records.bufflen,), dtype=c_int16)
                            status = self._set_data_buffers(line=line, buffer_max=self._records.buffers[line][m].ctypes,
                                                            buffer_min=None, bufflen=self._records.bufflen, segment=0,
                                                            mode=self._records.modes[m])
                if status != pico_num("PICO_OK"):
                    return status
            interval = c_uint32(interval)
            status = self._run_streaming(ref_interval=byref(interval), units=units,
                                         pretrig=pretrigger, posttrig=postrigger, autostop=(limit > 0),
                                         ratio=downsample, mode=mode, overview=bufflen)
            if status != pico_num("PICO_OK"):
                return status
            self._records.interval = interval.value
            try:
                self._recording_thread = Thread(target=self._recording_worker, args=(None,))
                if self._recording_event.is_set():
                    self._recording_event.clear()
                self._recording_thread.start()
            except Exception as ex:
                if not self._recording_event.is_set():
                    self._recording_event.set()
                self.last_error = ex.message
                print "Streaming Start(%d):" % sys.exc_info()[-1].tb_lineno, self.last_error, type(ex)
                return pico_num("PICO_STREAMING_FAILED")
            return pico_num("PICO_OK")

    def _run_streaming(self, ref_interval, units, pretrig, posttrig, autostop, ratio, mode, overview):
        return ldlib.RunStreaming(self._chandle, ref_interval, c_int32(units), c_uint32(pretrig), c_uint32(posttrig),
                                  c_int16(autostop), c_uint32(ratio), c_int32(mode), c_uint32(overview))

    @staticmethod
    def _make_chapter_tag():
        return time.strftime("%Y%m%d_%H%M%S")

    def stop_recording(self):
        """ Stops recording (Thanks, Captain Obvious !!!)
        :returns: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if self._recording_thread is None or not self._recording_thread.is_alive():
            return pico_num("PICO_NOT_USED_IN_THIS_CAPTURE_MODE")
        with self._recording_lock:
            self._recording_event.set()
        self._recording_thread.join()
        self._recording_thread = None
        return pico_num("PICO_OK")

    def _recording_worker(self, *args):
        """ Worker used in Streaming Collections """
        try:
            """ setup callback """
            self._recording_cb_type = self._streaming_ready()
            self._recording_cb_func = self._recording_cb_type(self._recording_cb)

            while not self._recording_event.is_set():
                with self._recording_lock:
                    s = ldlib.GetStreamingLatestValues(self._chandle, self._recording_cb_func, None)
                    if s not in (pico_num("PICO_OK"), pico_num("PICO_BUSY")) \
                            or (self._tape is not None and not self._tape.is_processing()):
                        break
            ldlib.Stop(self._chandle)
            if self._tape is not None:
                self._tape.record(None)
        except Exception as ex:
            self.last_error = ex.message
            print "Streaming Worker(%d):" % sys.exc_info()[-1].tb_lineno, self.last_error, type(ex)
        finally:
            with self._recording_lock:
                self._recording_event.clear()

    def _recording_cb(self, handle, samples, start, overflow, triggp, triggd, auto, param):
        """ Callback function called from within GetLatestValues """
        try:
            if auto == 1:
                self._recording_event.set()
                if self._leavers is not None and self._leavers.samples > 0 and self._tape is not None:
                    self._leavers.final = True
                    self._tape.record(self._leavers)
                    self._leavers = None
                return
            if len(self._records) == 0:
                return
            self._records.samples = samples
            self._records.start = start
            self._records.timestamp = time.time()
            for chann in self._records.buffers:
                self._records.buffers[chann]["overflow"] = overflow & 1 << chann > 0
            if self._records.triggerSet:
                if triggd != 0:
                    self._records.triggerAt = triggp
                    self._records.triggered = True
                else:
                    self._records.triggerAt = - 1
                    self._records.triggered = False
            if self._tape is not None:
                if self._leavers is not None:
                    left = self._leavers.top_up(self._records)
                    if self._leavers.bufflen == self._leavers.samples:
                        self._tape.record(self._leavers)
                        self._leavers = left
                else:
                    if self._records.bufflen == self._records.samples:
                        self._tape.record(self._records)
                    else:
                        self._leavers = self._records.side_copy()

        except Exception as ex:
            self.last_error = ex.message
            print "Streaming Callback(%d):" % sys.exc_info()[-1].tb_lineno, self.last_error, type(ex)

    def get_stored_data(self, mode, downsample, segments=None):
        """ Dumps current contents of the memory, different downsample modes can be selected
        :param mode: DownSample mode form RatioModes
        :type mode: int
        :param downsample: downsample bin size
        :type downsample: int
        :param segments: segment(s) numbers to flush, id None = streaming data is returned
        :type segments: int, tuple, None
        :return: status of the call with data as dict struct {segment: { channel: { data: np.array() } } }
        :rtype: tuple(int, dict)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE"), None
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                return pico_num("PICO_BUSY"), None
        modes = self.m.RatioModes.mode2dict(mode)
        if len(modes) == 0:
            return pico_num("PICO_RATIO_MODE_NOT_SUPPORTED"), None
        channels = [c for c in self._channel_set.keys() if self._channel_set[c].enabled]
        ports = [p for p in self._port_set.keys() if self._port_set[p].enabled]
        if len(channels) == 0 and len(ports) == 0:
            return pico_num("PICO_INVALID_CHANNEL"), None
        if segments is None:
            stream = True
            segments = (0,)
            samples = c_uint32(0)
            status = ldlib.NoOfStreamingValues(self._chandle, byref(samples))
            if status != pico_num("PICO_OK"):
                return status, None
            if samples.value == 0:
                return pico_num("PICO_DATA_NOT_AVAILABLE")
            samples = samples.value
        else:
            stream = False
            samples = int(self.info.memps / len(channels + ports))
        if isinstance(segments, int):
            segments = (segments,)
        data = {}
        with self._async_lock:
            for s in segments:
                data[s] = {}
                for n in channels + ports:
                    data[s][n] = {}
                    for m in modes:
                        bufflen = samples if modes[m] == self.m.RatioModes.none else int(samples / downsample)
                        if modes[m] == self.m.RatioModes.agg:
                            data[s][n]["min"] = np.empty(bufflen, dtype=c_int16)
                            data[s][n]["max"] = np.empty(bufflen, dtype=c_int16)
                            status = self._set_data_buffers(line=n, buffer_max=data[s][n]["max"].ctypes,
                                                            buffer_min=data[s][n]["min"].ctypes, bufflen=bufflen,
                                                            segment=s, mode=modes[m])
                        else:
                            data[s][n][m] = np.empty(bufflen, dtype=c_int16)
                            status = self._set_data_buffers(line=n, buffer_max=data[s][n][m].ctypes, buffer_min=None,
                                                            bufflen=bufflen, segment=s, mode=modes[m])
                        if status != pico_num("PICO_OK"):
                            return status, None
                try:
                    if stream:
                        self._async_cb_type = self._streaming_ready()
                    else:
                        self._async_cb_type = self._data_ready()
                    self._async_cb_func = self._async_cb_type(self._async_cb)
                    if self._async_event.is_set():
                        self._async_event.clear()
                    status = self._get_values_async(start=0, samples=samples, ratio=downsample, mode=mode,
                                                    segment=s, ref_cb=self._async_cb_func, ref_cb_param=None)
                except Exception as ex:
                    self.last_error = ex.message
                    print "Async Data(%d):" % sys.exc_info()[-1].tb_lineno, self.last_error, type(ex)
                    if not self._async_event.is_set():
                        self._async_event.set()
                    status = pico_num("PICO_OPERATION_FAILED")

                if status != pico_num("PICO_OK"):
                    if self._async_event.is_set():
                        self._async_event.clear()
                    return status, None
                self._async_event.wait()
                for n in channels + ports:
                    for m in modes:
                        self._set_data_buffers(line=n, buffer_max=None, buffer_min=None,
                                               bufflen=samples, segment=s, mode=modes[m])
        if self._async_event.is_set():
            self._async_event.clear()
        return pico_num("PICO_OK"), data

    def _async_cb(self, *param):
        """ Callback function for async device data """
        try:
            if self._async_event is not None:
                self._async_event.set()
        except:
            return

    def _get_values_async(self, start, samples, ratio, mode, segment, ref_cb, ref_cb_param):
        return ldlib.GetValuesAsync(self._chandle, c_uint32(start), c_uint32(samples), c_uint32(ratio), c_int32(mode),
                                    c_uint32(segment), ref_cb, ref_cb_param)

    def ets_setup(self, mode, cycles, interleaves):
        """ Configures ETS collection parameters
        :param mode: ETS mode as in ETSModes
        :type mode: int
        :param cycles: number of cycles to store
        :type cycles: int
        :param interleaves: number of uniform collection sets to use
        :type interleaves: int
        :returns: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if mode not in self.m.ETSModes.map:
            return pico_num("PICO_ETS_NOT_SUPPORTED")
        if interleaves > cycles:
            return pico_num("PICO_INVALID_PARAMETER")
        self._ets.mode = mode
        self._ets.cycles = cycles
        self._ets.interleaves = interleaves
        return pico_num("PICO_OK")

    def get_ets_status(self):
        """ Returns status of latest ETS collection
        :returns: status and collection interval in picoseconds
        :rtype: tuple(int, int)
        """
        return self._ets.status, self._ets.picos

    def set_simple_trigger(self, enabled, source, threshold, direction, delay=0, waitfor=0):
        """ Sets simple trigger (Doh...). If Advanced already on - remove it.
        :param enabled: enable the trigger or... not. hm...
        :type enabled: bool
        :param source: trigger channel/source as in TriggerChannels
        :type source: int
        :param threshold: vertical ratio of the current channel range as value from <-1.0, 1.0>
        :type threshold: float
        :param direction: trigger direction as in TriggerChannelDirections
        :type direction: int
        :param delay: delay trigger detection by times of sample interval
        :type delay: int
        :param waitfor: autotrigger time in miliseconds, 0 to wait for eva...
        :type waitfor: int
        :returns: status of the calls
        :rtype int:
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if True in [c.is_set() for c in self.trigger_conditions]:
            self.set_advanced_trigger(conditions=None)
        if True in [c.is_set() for c in self.pwq_conditions]:
            self.set_pwq_trigger(conditions=None)
        adc = int((threshold * 1.0 - int(threshold * 0.999999)) * self.info.max_adc)
        status = ldlib.SetSimpleTrigger(self._chandle, c_int16(enabled), c_int32(source), c_int16(adc),
                                        c_int32(direction), c_uint32(delay), c_int16(waitfor))
        if status == pico_num("PICO_OK"):
            self.trigger = enabled
            self.trigg_source = source
            self.trigg_threshold = threshold
            self.trigg_direction = direction
        return status

    def set_horizontal_trigger_ratio(self, ratio):
        """ Sets horizontal ration of Trigger Events
        :param ratio: collection block ratio to set trigger to as in <0.0, 1.0>
        :type ratio: float
        :returns: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        self.trigg_ratio = abs(ratio) % 1.000000001
        return pico_num("PICO_OK")

    def create_trigger_channel_properties(self, channel, upperbound=0.5, upperhys=0.25, lowerbound=-0.5, lowerhys=0.25,
                                          mode=None, direction=None):
        """ (helper) Constructs TriggerProperty object
        :param channel: Channel enum from TriggerChannels
        :type channel: int
        :param upperbound: upper threshold point as a ratio of whole channel in range <-1.0, 1.0>
        :type upperbound: float
        :param upperhys: upper threshold hysteresis parameter as a ratio of whole channel in range <0.0, 1.0>
        :type upperhys: float
        :param lowerbound: lower threshold point as a ratio of whole channel in range <-1.0, 1.0>
        :type lowerbound: float
        :param lowerhys: lower threshold hysteresis parameter as a ratio of whole channel in range <0.0, 1.0>
        :type lowerhys: float
        :param mode: Enum from ThresholdModes
        :type mode: int
        :param direction: Enum from ThresholdDirections
        :type direction: int
        :return: Trigger properties object with values set to match current device
        :rtype: TriggerChannelProperties
        """
        if self._handle <= 0 \
                or mode not in self.m.ThresholdModes.map \
                or direction not in self.m.ThresholdDirections.map:
            return None

        if mode is None:
            mode = self.m.ThresholdModes.window

        if direction is None:
            direction = self.m.ThresholdDirections.enter

        return self.m.TriggerChannelProperties(
            channel=channel,
            threshUpperADC=int((upperbound * 1.0 - int(upperbound * 0.999999)) * self.info.max_adc),
            threshUpperHys=int((abs(float(upperhys)) % 1) * 2 * self.info.max_adc),
            threshLowerADC=int((lowerbound * 1.0 - int(lowerbound * 0.999999)) * self.info.max_adc),
            threshLowerHys=int((abs(float(lowerhys)) % 1) * 2 * self.info.max_adc),
            threshMode=mode, direction=direction)

    def set_advanced_trigger(self, conditions=None, analog=None, digital=None, waitfor=0):
        """ Passes advanced triggering setup to the driver
        :param conditions: tuple of TriggerConditions objects, they are joined by OR operand. None to turn off
        :type conditions: tuple, None
        :param analog: tuple of TriggerChannelProperties objects, None to ignore all
        :type analog: tuple, None
        :param digital: tuple of tuple pairs (bit, trigger digital direction)
        :type digital: tuple, None
        :param waitfor: time in miliseconds, how long to wait for trigger to occur. If 0 - indefinitely
        :param waitfor: int
        :return: final status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")

        conditions = conditions if conditions is not None else ()
        analog = analog if analog is not None else ()
        digital = digital if digital is not None and self.info.num_ports > 0 else ()

        if not isinstance(conditions, (tuple, list)):
            return pico_num("PICO_INVALID_CONDITION_INFO")
        if not isinstance(analog, (tuple, list)):
            return pico_num("PICO_INVALID_TRIGGER_PROPERTY")
        if not isinstance(digital, (tuple, list)):
            return pico_num("PICO_INVALID_DIGITAL_TRIGGER_DIRECTION")
        # turn off simple trigger if present:
        if self.trigger:
            status = self.set_simple_trigger(enabled=False, source=self.trigg_source,
                                             threshold=self.trigg_threshold, direction=self.trigg_direction)
            if status != pico_num("PICO_OK"):
                return status
        # load analog  properties and directions first
        analogout = ()
        analogdir = self.m.TriggerChannelDirections()
        if len(analog) > 0:
            # scan and discards duplicates
            triggchans = ()
            for p in analog:
                if not isinstance(p, self.m.TriggerChannelProperties) or p.channel not in self.m.TriggerChannels.map:
                    continue
                if p.channel not in triggchans:
                    triggchans += (p.channel,)

                    if p.direction in self.m.ThresholdDirections.map:
                        analogdir[self.m.TriggerChannels.labels[p.channel]] = p.direction
                    else:
                        analogdir[self.m.TriggerChannels.labels[p.channel]] = self.m.ThresholdDirections.none
                        p.direction = self.m.ThresholdDirections.none
                    analogout += (p,)
        if len(analogout) > 0:
            analogprops = cast(((self.m.TriggerChannelPropertiesStruct * len(analogout))()),
                               POINTER(self.m.TriggerChannelPropertiesStruct))
            for i in range(0, len(analogout)):
                analogprops[i] = analogout[i].to_struct()
        else:
            analogprops = None

        status = ldlib.SetTriggerChannelDirections(
            self._chandle,
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.A]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.B]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.C]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.D]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.Ext]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.Aux]])
        )
        if status != pico_num("PICO_OK"):
            return status

        status = ldlib.SetTriggerChannelProperties(
            self._chandle, analogprops, c_int16(len(analogout)), c_int16(0), c_int32(waitfor))
        if status != pico_num("PICO_OK"):
            return status
        # now do the digital
        digitalout = ()
        if len(digital) > 0 and self.info.num_ports > 0:
            triggbits = ()
            for d in digital:
                if not isinstance(d, tuple) \
                        or len(d) != 2 or d[0] in triggbits \
                        or True not in [d[0] in t for t in self.m.PortBits.map[:self.info.num_ports]] \
                        or d[1] not in self.m.DigitalDirections.map:
                    continue
                digitalout += (d,)
                triggbits += (d[0],)
        if len(digitalout) > 0:
            digitaldirs = cast(((self.m.DigitalChannelDirectionStruct * len(digitalout))()),
                               POINTER(self.m.DigitalChannelDirectionStruct))
            for i in range(0, len(digitalout)):
                digitaldirs[i].portbit = digitalout[i][0]
                digitaldirs[i].direction = digitalout[i][1]
        else:
            digitaldirs = None
        if self.info.num_ports > 0:
            status = ldlib.SetTriggerDigitalPortProperties(self._chandle, digitaldirs, c_int16(len(digitalout)))
            if status != pico_num("PICO_OK"):
                return status
        # finally do the conditions
        conditionsout = ()
        if len(conditions) > 0:
            for c in conditions:
                if not isinstance(c, self.m.TriggerConditions) or not c.is_set():
                    continue
                conditionsout += (c,)
        if len(conditionsout) == 0:
            conditionsout += (self.m.TriggerConditions(),)
        conds = \
            cast(((self.m.TriggerConditionsStruct * len(conditionsout))()), POINTER(self.m.TriggerConditionsStruct))
        for i in range(0, len(conditionsout)):
            conds[i] = conditionsout[i].to_struct()
        status = ldlib.SetTriggerChannelConditions(self._chandle, conds, c_int16(len(conditionsout)))
        if status != pico_num("PICO_OK"):
            return status
        self.trigger_conditions = conditionsout
        self.trigger_analog = analogout
        self.trigger_digital = digitalout
        return pico_num("PICO_OK")

    def set_pwq_trigger(self, conditions=None, direction=None, lower=0, upper=0, pwqtype=0):
        """ Pulse width qualifier trigger setup
        :param conditions: tuple PwqConditions objects, they are joined by OR operand. None to turn off.
        :type conditions: tuple, None
        :param direction: Qualifier direction from ThresholdDirections
        :type direction: int
        :param lower: lower sample count
        :type lower: int
        :param upper: upper sample count
        :type upper: int
        :param pwqtype: Qualifier type from PwqTypes
        :type pwqtype: int
        :return: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")

        if direction is None:
            direction = self.m.ThresholdDirections.rising

        conditions = conditions if conditions is not None else ()
        if not isinstance(conditions, (tuple, list)):
            return pico_num("PICO_INVALID_CONDITION_INFO")
        if direction not in self.m.ThresholdDirections.map:
            return pico_num("PICO_INVALID_TRIGGER_DIRECTION")
        if pwqtype not in self.m.PwqTypes.map:
            return pico_num("PICO_PULSE_WIDTH_QUALIFIER")
        if self.trigger:
            status = self.set_simple_trigger(enabled=False, source=self.trigg_source,
                                             threshold=self.trigg_threshold, direction=self.trigg_direction)
            if status != pico_num("PICO_OK"):
                return status

        condout = ()
        for c in conditions:
            if not isinstance(c, self.m.PwqConditions) or not c.is_set():
                continue
            condout += (c,)
        if len(condout) == 0:
            condout += (self.m.PwqConditions(),)
        conds = cast(((self.m.PwqConditionsStruct * len(condout))()), POINTER(self.m.PwqConditionsStruct))
        for i in range(0, len(condout)):
            conds[i] = condout[i].to_struct()

        status = ldlib.SetPulseWidthQualifier(self._chandle, conds, c_int16(len(condout)), c_int32(direction),
                                              c_uint32(lower), c_uint32(upper), c_int32(pwqtype))
        if status != pico_num("PICO_OK"):
            return status
        self.pwq_conditions = condout
        self.pwq_direction = direction
        self.pwq_lower = lower
        self.pwq_upper = upper
        self.pwq_type = pwqtype
        return pico_num("PICO_OK")

    def get_trigger_info(self):
        """
        :return: Dictionary with the following trigger information:
        {
            condtions: tuple,
            analog: tuple,
            digital: tuple,
            waitfor: int
        }
        """
        return dict2class(conditions=self.trigger_conditions, analog=self.trigger_analog,
                          digital=self.trigger_digital, waitfor=self.trigg_wait)

    def get_pwq_trigger_info(self):
        """
        :return: Dictionary with the following pwq trigger information:
        {
            condition: tuple
            direction: int
            lower: int
            upper: int
            pwqtype: int
        }
        """
        return dict2class(conditions=self.pwq_conditions, direction=self.pwq_direction,
                          lower=self.pwq_lower, upper=self.pwq_upper, pwqtype=self.pwq_type)

    def is_trigger_set(self):
        """ Checks whether trigger is set for the next collection
        :returns: result of the check
        :rtype: bool
        """
        if self._handle <= 0:
            return None
        return self.trigger or (True in [c.is_set() for c in self.trigger_conditions])

    def get_trigger_time_offset(self, segment):
        """ Returns time offset in nanoseconds that occurred in the specified segment
        :param segment: memory segment number
        :type segment: int
        :returns: status of the call, offset
        :rtype: tuple(int, float)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if segment > self._segments:
            return pico_num("PICO_SEGMENT_OUT_OF_RANGE")
        offt = c_int64()
        unit = c_uint32()
        status = self._get_trigger_time_offset(ref_offsets=byref(offt), ref_units=byref(unit), segment=segment)
        if status != pico_num("PICO_OK"):
            return status, None
        return status, time.value * float(pow(10, TimeUnits.nanofactors(unit.value)))

    def _get_trigger_time_offset(self, ref_offsets, ref_units, segment):
        return ldlib.GetTriggerTimeOffset(self._chandle, ref_offsets, ref_units, c_uint32(segment))

    def stop(self):
        """ Stops any pending activities on the device
        :returns: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                e.set()
        return ldlib.Stop(self._chandle)

    def close_unit(self):
        """ Closes currently open unit
        :returns: status of the call
        :rtype: int
        """
        if self._handle > 0:
            self.stop()
            self.release_all_buffers()
            status = ldlib.CloseUnit(self._chandle)
            if status == pico_num("PICO_OK"):
                self._handle = 0
                self._chandle.value = 0
        else:
            status = pico_num("PICO_INVALID_HANDLE")
        return status

    def set_simple_sig_gen(self, wave_type, frequency, pk2pk, offset=0):
        """ Controls setup of simple signal generator
        :param wave_type: wave type enum as in WaveTypes
        :type wave_type: int
        :param frequency: frequency in Hz of the signal to generate
        :type frequency: float
        :param pk2pk: signal amplitude in microvolts
        :type pk2pk: int
        :param offset: zero offset of the generated signal, in microvolts
        :type offset: int
        :returns: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if self.info.has_siggen:
            return self._set_sig_gen_built_in(offset=offset, pk2pk=pk2pk, wave=wave_type,
                                              start=frequency, stop=frequency, increment=0, dwelltime=0,
                                              sweep=self.m.SweepTypes.up, extra=self.m.SigExtra.off, shots=0, sweeps=0,
                                              trigt=self.m.SigTriggerTypes.falling, trigs=self.m.SigTriggerSource.none,
                                              threshold=0)
        else:
            return pico_num("PICO_NO_SIGNAL_GENERATOR")

    def _set_sig_gen_built_in(self, offset, pk2pk, wave, start, stop, increment, dwelltime,
                              sweep, extra, shots, sweeps, trigt, trigs, threshold):

        return ldlib.SetSigGenBuiltIn(self._chandle, c_int32(offset), c_uint32(pk2pk), c_int16(wave),
                                      c_float(start), c_float(stop), c_float(increment), c_float(dwelltime),
                                      c_int32(sweep), c_int32(extra), c_uint32(shots), c_uint32(sweeps),
                                      c_int32(trigt), c_int32(trigs), c_int16(threshold))

    def set_awg_player(self, frequency, waveform, pk2pk, offset=0, mode=None):
        """ Setup AWG buffer player
        :param frequency: waveform buffer repeat frequency
        :type frequency: float
        :param waveform: one dimensional buffer containing a waveform, len up to awg_size, values in <-32767, 32768>
        :type waveform: tuple
        :param pk2pk: amplitude of the waveform in microvolts, final values clipped to +/-2V
        :type pk2pk: long, int
        :param offset: waveform offset in microvolts, final values clipped to +/-2V
        :type offset: long, int
        :param mode: waveform repeat index mode, defaults to single
        :type mode: int
        :returns: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if not self.info.has_awg:
            return pico_num("PICO_AWG_NOT_SUPPORTED")
        if not isinstance(waveform, tuple):
            return pico_num("PICO_INVALID_BUFFER")
        if mode not in self.m.IndexModes.map:
            return pico_num("PICO_INVALID_BUFFER")

        if mode is None:
            mode = self.m.IndexModes.single

        phase = c_uint32(0)

        status = ldlib.SigGenFrequencyToPhase(self._chandle, c_double(frequency),
                                              c_int32(mode), c_uint32(len(waveform)), byref(phase))
        if status != pico_num("PICO_OK"):
            return status
        wave = np.array([self.info.awg_min if v < self.info.awg_min else
                         (self.info.awg_max if v > self.info.awg_max else v)
                         for v in waveform], dtype=c_int16)

        return self._set_sig_gen_arbitrary(offset=offset, pk2pk=pk2pk, phase_start=phase.value, phase_stop=phase.value,
                                           phase_inc=0, dwell=0, ref_wave=wave.ctypes, bufflen=len(waveform),
                                           sweep=self.m.SweepTypes.up, extra=self.m.SigExtra.off, mode=mode,
                                           shots=0, sweeps=0, trigt=self.m.SigTriggerTypes.rising,
                                           trigs=self.m.SigTriggerSource.none, threshold=0)

    def _set_sig_gen_arbitrary(self, offset, pk2pk, phase_start, phase_stop, phase_inc, dwell, ref_wave, bufflen,
                               sweep, extra, mode, shots, sweeps, trigt, trigs, threshold):
        return ldlib.SetSigGenArbitrary(self._chandle, c_int32(offset), c_uint32(pk2pk), c_uint32(phase_start),
                                        c_uint32(phase_stop), c_uint32(phase_inc), c_uint32(dwell), ref_wave,
                                        c_int32(bufflen), c_int32(sweep), c_int32(extra), c_int32(mode),
                                        c_uint32(shots), c_uint32(sweeps), c_int32(trigt), c_int32(trigs),
                                        c_int16(threshold))

    def ping_unit(self):
        """ Checks if current device is alive
        :returns: status PICO_OK if alive
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        return ldlib.PingUnit(self._chandle)

    @staticmethod
    def _block_ready():
        if sys.platform == "win32":
            return WINFUNCTYPE(None, c_int16, c_uint32, c_void_p)
        else:
            return CFUNCTYPE(None, c_int16, c_uint32, c_void_p)

    @staticmethod
    def _streaming_ready():
        if sys.platform == "win32":
            return WINFUNCTYPE(None, c_int16, c_int32, c_uint32, c_int16, c_uint32, c_int16, c_int16, c_void_p)
        else:
            return CFUNCTYPE(None, c_int16, c_int32, c_uint32, c_int16, c_uint32, c_int16, c_int16, c_void_p)

    @staticmethod
    def _data_ready():
        if sys.platform == 'win32':
            return WINFUNCTYPE(None, c_int16, c_uint32, c_uint32, c_int16, c_void_p)
        else:
            return CFUNCTYPE(None, c_int16, c_uint32, c_uint32, c_int16, c_void_p)


def enumerate_units(loaded_lib):
    """ Module function for enumerating all devices served by this driver
    :param loaded_lib: dict2class object of loaded library bindings
    :type loaded_lib: dict2class
    :returns: list of serials of found devices
    :rtype: list, tuple
    """
    count = c_int16()
    length = c_int16(MAX_NUM_DEVICES * 10)
    serials = create_string_buffer(length.value)
    try:
        loaded_lib.EnumerateUnits(byref(count), serials, byref(length))
    except AttributeError:
            return ()
    if len(serials.value):
        return tuple(serials.value.split(","))
    else:
        return ()
