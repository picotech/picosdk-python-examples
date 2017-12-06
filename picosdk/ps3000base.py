#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Python calls for ps3000 based PicoScope devices.
"""

from picosdk.ps5000base import *
from psutils import *
from picosdk import ps5000base


class Info(dict2class):
    """ Retrofited device PICO_INFO set """
    driver_version = 0
    usb_version = 1
    hardware_version = 2
    variant_info = 3
    batch_and_serial = 4
    cal_date = 5
    error_code = 6
    kernel_version = 7
    map = (driver_version, usb_version, hardware_version, variant_info,
           batch_and_serial, cal_date, error_code, kernel_version)
    labels = {driver_version: "driver_version", usb_version: "usb_version", hardware_version: "hardware_version",
              variant_info: "variant_info", batch_and_serial: "batch_and_serial", cal_date: "cal_date",
              error_code: "error_code", kernel_version: "kernel_version"}


class TriggerChannels(dict2class):
    """ Collection of channels used in triggering """
    A = Channels.A
    B = Channels.B
    C = Channels.C
    D = Channels.D
    Ext = 4
    Off = 5
    map = (A, B, C, D, Ext)
    labels = {A: "A", B: "B", C: "C", D: "D", Ext: "EXT", Off: "NONE"}


class TriggerChannelDirections(dict2class):
    """ container for channel directions """

    def __init__(self, *args, **kwargs):
        for c in TriggerChannels.map:
            self.__dict__[TriggerChannels.labels[c]] = ThresholdDirections.none
            self.update(*args, **kwargs)


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
    rising_or_falling = 4
    above_lower = above
    below_lower = below
    rising_lower = rising
    falling_lower = falling
    positive_runt = rising
    negative_runt = falling
    map = (above, below, rising, falling, rising_or_falling)
    simple = (above, below, rising, falling)
    labels = {above: "above", below: "below", rising: "rising", falling: "falling", rising_or_falling: "rise/fall"}

    @staticmethod
    def to_simple(direction):
        """ Retrofitted translation from simple types to incomplete collection
        :param direction: advanced trigger direction
        :type direction: int
        :return: corresponding enum
        :rtype: int
        """
        if direction in (ThresholdDirections.above, ThresholdDirections.rising):
            return 0
        if direction in (ThresholdDirections.below, ThresholdDirections.falling):
            return 1
        else:
            return 2


class TriggerChannelPropertiesStruct(Structure):
    """ CType specifier for Trigger Channel Properties in Advanced Triggers """
    _fields_ = [
        ("threshUpperADC", c_int16),
        ("threshLowerADC", c_int16),
        ("hysteresis", c_uint16),
        ("channel", c_int16),
        ("threshMode", c_int32)
    ]
    _pack_ = 1


class TriggerChannelProperties(dict2class):
    """ Object describing single Channel Trigger Properties in Advanced Triggers """
    threshUpperADC = 0.2
    threshLowerADC = -32767
    hysteresis = 32767
    threshMode = ThresholdModes.level
    direction = ThresholdDirections.none

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        self.update(self, *args, **kwargs)

    def to_struct(self):
        return TriggerChannelPropertiesStruct(self.threshUpperADC, self.threshLowerADC,
                                              self.hysteresis, self.channel, self.threshMode)


class TriggerConditionsStruct(Structure):
    """ CType specifier for Trigger Conditions """
    _fields_ = [
        ("chA", c_int32),
        ("chB", c_int32),
        ("chC", c_int32),
        ("chD", c_int32),
        ("ext", c_int32),
        ("pwq", c_int32)
    ]
    _pack_ = 1


class TriggerConditions(dict2class):
    """ Collection of Trigger Conditions for Advanced Triggering """
    chA = TriggerState.dont_care
    chB = TriggerState.dont_care
    chC = TriggerState.dont_care
    chD = TriggerState.dont_care
    ext = TriggerState.dont_care
    pwq = TriggerState.dont_care

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def to_struct(self):
        return TriggerConditionsStruct(self.chA, self.chB, self.chC, self.chD, self.ext, self.pwq)

    def is_set(self):
        return len([c for c in
                    (self.chA, self.chB, self.chC, self.chD, self.ext, self.pwq)
                    if c != TriggerState.dont_care]) > 0


class PwqConditionsStruct(Structure):
    """ CType specifier for Pulse Width Qualifier Conditions """
    _fields_ = [
        ("chA", c_int32),
        ("chB", c_int32),
        ("chC", c_int32),
        ("chD", c_int32),
        ("ext", c_int32)
    ]
    _pack_ = 1


class PwqConditions(dict2class):
    """ Collection of Pulse Width Qualifier Conditions """
    chA = TriggerState.dont_care
    chB = TriggerState.dont_care
    chC = TriggerState.dont_care
    chD = TriggerState.dont_care
    ext = TriggerState.dont_care

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def to_struct(self):
        return PwqConditionsStruct(self.chA, self.chB, self.chC, self.chD, self.ext)

    def is_set(self):
        return len([c for c in
                    (self.chA, self.chB, self.chC, self.chD, self.ext)
                    if c != TriggerState.dont_care]
                   ) > 0


class PS3000Device(ps5000base.PS5000Device):
    def __init__(self, libobj):
        self.m = sys.modules[__name__]

        global ldlib
        ldlib = libobj

        self._handle = 0
        self._chandle = c_int16(0)
        self.info = UnitInfo()
        self._channel_set = {}
        self._port_set = {}
        self._buffers = {}
        self._segments = 0
        self._collect_event = Event()
        if self._collect_event.is_set():
            self._collect_event.clear()
        self._async_event = None
        self.trigger = False
        self.trigg_source = self.m.TriggerChannels.A
        self.trigg_threshold = 0.0
        self.trigg_direction = self.m.SigTriggerTypes.rising
        self.trigg_ratio = 0
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
        self._tape = None
        self._records = None
        self._recording_thread = None
        self._recording_lock = Lock()
        if self._recording_lock.acquire(False):
            self._recording_lock.release()
        self._recording_event = Event()
        if self._recording_event.is_set():
            self._recording_event.clear()
        self._recording_cb_type = None
        self._recording_cb_func = None
        self._recording_buffers = None
        self._recording_values = 0
        self._recording_overflow = 0
        self._recording_triggered = 0
        self._recording_trigger_at = 0

    def open_unit(self, serial=None):
        """ Opens unit
        :param serial: string specifying device serial and batch
        :type serial: string
        :returns: status of the call
        :rtype: int
        """
        if self._handle > 0:
            return pico_num("PICO_MAX_UNITS_OPENED")

        handles = ()
        found = 0
        while True:
            try:
                handle = ldlib.OpenUnit()
            except AttributeError:
                return pico_num("PICO_NOT_FOUND")
            if handle > 0:
                if serial is not None:
                    handles += (handle, )
                else:
                    self._handle = handle
                    self._chandle.value = handle
                    found = handle
                    break
            else:
                if serial is None or len(handles) == 0:
                    return pico_num("PICO_NOT_FOUND")
                else:
                    for handle in handles:
                        if found == 0:
                            info = create_string_buffer("\0", MAX_INFO_LEN)
                            info_len = ldlib.GetUnitInfo(c_int16(handle), info,
                                                         c_int16(MAX_INFO_LEN), c_int16(Info.batch_and_serial))
                            if info_len > 0:
                                if info.value == serial[:info_len]:
                                    self._handle = handle
                                    self._chandle.value = handle
                                    found = handle
                                    continue
                        ldlib.CloseUnit(c_int16(handle))
                break
        if found == 0:
            return pico_num("PICO_NOT_FOUND")
        else:
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

        self.info.handle = self._handle
        for info in Info.map:
            line = create_string_buffer("\0", MAX_INFO_LEN)
            line_len = ldlib.GetUnitInfo(self._chandle, line, c_int16(MAX_INFO_LEN), c_int16(info))
            if line_len > 0:
                self.info[Info.labels[info]] = line[:line_len]
            else:
                self.info[Info.labels[info]] = None
        self.info.firmware_version_1 = 0
        self.info.firmware_version_2 = self.info.kernel_version
        if self.info.variant_info is not None:
            status = self._set_variant_info()
        else:
            status = pico_num("PICO_INFO_UNAVAILABLE")
        if status != pico_num("PICO_OK"):
            return status
        self.info.channel_ranges = dict2class()
        inner = False
        outer = False
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
            r.max_dc_offset = None
            r.min_dc_offset = None
            r.max_ac_offset = None
            r.min_ac_offset = None
            self.info.channel_ranges[i] = r
        self.info.min_adc = -32767
        self.info.max_adc = 32767
        self.info.nan_adc = -32768
        self.info.awg_min = 0
        self.info.awg_max = 255
        return pico_num("PICO_OK")

    def _set_variant_info(self):
        return pico_num("PICO_INFO_UNAVAILABLE")

    def _set_memory_info(self):
        """ No need to set up memory in these devices
        :returns: PICO_OK
        :rtype: int
        """
        self._segments = 1
        return pico_num("PICO_OK")

    def set_defaults(self, filename=None):
        """ Sets device into default state
        :returns: status of subsequent calls
        :rtype: int
        """
        # TODO implement storing/loading setting from file
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")

        for channel in range(0, self.info.num_channels):
            state = self.m.ChannelState()
            state.enabled = False
            state.coupling = self.m.Couplings.dc
            state.range = self.m.Ranges.r500mv
            state.offset = 0
            self.set_channel(self.m.Channels.map[channel], state)
        return pico_num("PICO_OK")

    def flash_led(self, count=1):
        """ Flashes device's LED count times
        :param count: number of flashes
        :type count: int
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        while count > 0:
            status = ldlib.FlashLed(self._chandle)
            if status == 0:
                return pico_num("PICO_INVALID_PARAMETER")
            count -= 1
        return pico_num("PICO_OK")

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
        dc = 1 if state.coupling == self.m.Couplings.dc else 0
        status = ldlib.SetChannel(self._chandle, c_int16(channel), c_int16(state.enabled),
                                  c_int16(dc), c_int16(state.range))
        if status == 0:
            return pico_num("PICO_INVALID_PARAMETER")
        state.overvoltaged = False
        self._channel_set[channel] = deepcopy(state)
        return pico_num("PICO_OK")

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
        self._segments = segments
        self.info.memps = self.info.memory
        return pico_num("PICO_OK"), self.info.memory

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
        if self.info.has_adv_trigger:
            if True in [c.is_set() for c in self.trigger_conditions]:
                self.set_advanced_trigger(conditions=None)
            if True in [c.is_set() for c in self.pwq_conditions]:
                self.set_pwq_trigger(conditions=None)
        adc = int((threshold * 1.0 - int(threshold * 0.999999)) * self.info.max_adc)
        status = ldlib.SetTrigger(self._chandle, c_int16(source if enabled else self.m.TriggerChannels.Off),
                                  c_int16(adc), c_int16(self.m.ThresholdDirections.to_simple(direction)),
                                  c_float(-100.0 * self.trigg_ratio), c_int16(waitfor))
        if status != 0:
            self.trigger = enabled
            self.trigg_source = source
            self.trigg_threshold = threshold
            self.trigg_direction = direction
            self.trigg_wait = waitfor
            return pico_num("PICO_OK")
        return pico_num("PICO_INVALID_PARAMETER")

    def set_horizontal_trigger_ratio(self, ratio):
        """ Sets horizontal ration of Trigger Events
        :param ratio: collection block ratio to set trigger to as in <0.0, 1.0>
        :type ratio: float
        :returns: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")

        ratio = abs(ratio) % 1
        if ratio != self.trigg_ratio:
            if self.trigger:
                adc = int((self.trigg_threshold * 1.0 - int(self.trigg_threshold * 0.999999)) * self.info.max_adc)
                status = ldlib.SetTrigger(self._chandle, c_int16(self.trigg_source), c_int16(adc),
                                          c_int16(self.m.ThresholdDirections.to_simple(self.trigg_direction)),
                                          c_float(-100.0 * ratio), c_int16(self.trigg_wait))
                if status == 0:
                    return pico_num("PICO_INVALID_PARAMETER")
            elif self.info.has_adv_trigger and (True in [c.is_set() for c in self.trigger_conditions]):
                status = ldlib.SetAdvTriggerDelay(self._chandle, c_uint32(0), c_float(-100.0 * ratio))
                if status == 0:
                    return pico_num("PICO_INVALID_PARAMETER")
            self.trigg_ratio = ratio
        return pico_num("PICO_OK")

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
        if bulk or overlapped:
            return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")
        if segment > self._segments:
            return pico_num("PICO_SEGMENT_OUT_OF_RANGE")

        """ We expect only one collection at the time """
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                return pico_num("PICO_BUSY")

        """ Locate buffers taking part in collection """
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
                                                c_int16(self._ets.cycles), c_int16(self._ets.interleave), None)
                if self._ets.status == pico_num("PICO_OK"):
                    self._ets.last = self.m.ETSModes.off
            elif (self.trigger or True in [c.is_set() for c in (self.trigger_conditions + self.pwq_conditions)]) \
                    and len([1 for p in self._port_set.keys() if self._port_set[p].enabled]) == 0:
                picos = c_int32(0)
                self._ets.status = ldlib.SetEts(self._chandle, c_int32(self._ets.mode), c_int16(self._ets.cycles),
                                                c_int16(self._ets.interleave), byref(picos))
                if self._ets.status == pico_num("PICO_OK"):
                    self._ets.last = self._ets.mode
                    self._ets.picos = picos.value

        if self._ets.last != self.m.ETSModes.off:
            timebase = 1

        """ calculate timebase from interval """
        finterval = c_int32(0)
        linterval = c_int32(0)

        if isinstance(interval, float):
            interval = int(interval)

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

        for index in indexes:
            with self._buffers[index].access_lock:
                self._buffers[index].last_interval = interval
                self._buffers[index].last_timebase = timebase
                self._buffers[index].real_interval = finterval.value
            self._lock_buffer(index)

        if event_handle is not None:
            self._collect_event = event_handle
        if self._collect_event.is_set():
            self._collect_event.clear()
        try:
            self._collect_event.set()
            to_sleep = (interval * samples / 5.0) / 1000000000
            status = ldlib.RunBlock(self._chandle, c_int32(samples), c_int16(timebase), c_int16(1), None)
            if status == 0:
                return pico_num("PICO_INVALID_PARAMETER")
            while True:
                if not self._collect_event.is_set():
                    break
                status = ldlib.Ready(self._chandle)
                if status < 0:
                    return pico_num("PICO_NOT_RESPONDING")
                elif status > 0:
                    self._collect_event.clear()
                    break
                sleep(to_sleep)
        finally:
            self._collect_event.clear()
        buffers = {}
        handles = {}
        aggregates = {}
        averages = {}
        decimates = {}
        for c in self.m.Channels.map:
            if c in self._channel_set.keys() and self._channel_set[c].enabled:
                buffers[c] = np.empty(samples, c_int16)
                handles[c] = buffers[c].ctypes
            else:
                buffers[c] = None
                handles[c] = None
        overvoltaged = c_int16(0)
        status = ldlib.GetValues(self._chandle,
                                 handles[self.m.Channels.A], handles[self.m.Channels.B],
                                 handles[self.m.Channels.C], handles[self.m.Channels.D],
                                 byref(overvoltaged), c_int32(samples))
        if status == 0:
            return pico_num("PICO_INVALID_PARAMETER")
        for index in indexes:
            with self._buffers[index].access_lock:
                c = self._buffers[index].channel
                if self._buffers[index].mode == self.m.RatioModes.raw:
                    self._buffers[index].data = buffers[c]
                else:
                    if buffers[c] is not None:
                        l = int(samples / self._buffers[index].downsample) * self._buffers[index].downsample
                        t = buffers[c][:l].reshape(-1, self._buffers[index].downsample)
                    if self._buffers[index].mode == self.m.RatioModes.agg:
                        if c not in aggregates.keys():
                            aggregates[c] = {"max": None, "min": None}
                            if buffers[c] is not None:
                                aggregates[c]["max"] = t.max(axis=1)
                                aggregates[c]["min"] = t.min(axis=1)
                        self._buffers[index].data = aggregates[c]["max"]
                        self._buffers[index].data_min = aggregates[c]["min"]
                    elif self._buffers[index].mode == self.m.RatioModes.avg:
                        if c not in averages.keys():
                            averages[c] = None
                            if buffers[c] is not None:
                                averages[c] = t.mean(axis=1)
                        self._buffers[index].data = averages[c]
                    elif self._buffers[index].mode == self.m.RatioModes.dec:
                        if c not in decimates.keys():
                            decimates[c] = None
                            if buffers[c] is not None:
                                decimates[c] = t[:, 0]
                        self._buffers[index].data = decimates[c]
                self._channel_set[c].overvoltaged = overvoltaged.value & (1 << c) != 0

        return pico_num("PICO_OK")

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
        :return: picostatus number of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")

    def collect_segment_overlapped(self, segment, interval=None, event_handle=None, timebase=None, block=True):
        """
        Runs Block data collection on(from) given segment in overlapped setup.
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")

    def set_overlapped_buffers(self, indexes):
        """ Preallocate collection buffers in overlapped mode
        :param indexes: list of buffer indexes to preallocate
        :type indexes: list, tuple
        :return: status of the calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")

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
            """ Gather how many channels are enabled """
            channels = [c for c in self._channel_set.keys() if self._channel_set[c].enabled]
            """ none of the channels are enabled """
            if len(channels) == 0:
                return pico_num("PICO_INVALID_CHANNEL")
            """ initialize records """
            self._records = StreamingTapeRecording()
            self._records.device = self.info.variant_info
            self._records.serial = self.info.batch_and_serial
            """ Determine how many ratio modes to set up """
            self._records.modes = self.m.RatioModes.mode2dict(mode)
            # overview buff len
            if memlength == 0:
                if limit == 0:
                    # half a second of data
                    desired = int(interval *
                                  self.m.TimeUnits.multiplier(units, self.m.TimeUnits.multiplier.s) *
                                  ceil(len(channels) / 2.0))
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
            self._records.enabled = len(channels)
            self._records.units = units
            self._records.mode = mode
            self._records.downsample = downsample
            self._records.bufflen = bufflen
            self._records.max_samples = samples
            if limit > 0:
                self._records.final = False
            self._records.autostop = limit > 0
            self._records.buffers = {}
            self._records.interval = interval
            triggadv = self.info.has_adv_trigger and (True in [c.is_set() for c in self.trigger_conditions])
            triggpwq = self.info.has_adv_trigger and (True in [c.is_set() for c in self.pwq_conditions])
            if self.trigger or triggadv or triggpwq:
                self._records.triggerSet = True
                self._records.triggered = False
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
            """ prepare buffers templates """
            for c in channels:
                self._records.buffers[c] = {}
                self._records.buffers[c]["range"] = self._channel_set[c].range
                self._records.buffers[c]["scale"] = self.m.Ranges.values[self._channel_set[c].range]
                if self._records.mode == self.m.RatioModes.raw:
                    self._records.buffers[c]["raw"] = None
                else:
                    for m in self._records.modes:
                        if self._records.modes[m] == self.m.RatioModes.agg:
                            self._records.buffers[c]["min"] = None
                            self._records.buffers[c]["max"] = None
                        else:
                            self._records.buffers[c][m] = None
            status = self._start_streaming()
        return status

    def _start_streaming(self):
        if self.info.has_fast_streaming:
            return self._start_fast_streaming()
        else:
            return self._start_compatible_streaming()

    def _start_compatible_streaming(self):
        interval = int(self._records.interval * self.m.TimeUnits.multiplier(self._records.units, self.m.TimeUnits.ms))
        interval = max(1, min(interval, 65535))
        status = ldlib.RunCompatibleStreaming(self._chandle, c_int16(interval),
                                              c_int32(min(self._records.max_samples, 60000)), c_int16(0))
        if status == 0:
            return pico_num("PICO_STREAMING_FAILED")
        self._records.interval = interval
        self._records.units = self.m.TimeUnits.ms
        try:
            self._recording_thread = Thread(target=self._compatible_recording_worker, args=(None,))
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

    def _compatible_recording_worker(self, *args):
        buffers = {}
        handles = {}
        buckets = {}
        cut_off = int(self._records.max_samples / self._records.downsample) * self._records.downsample
        fill_level = 0
        window_ov = 0
        for c in self.m.Channels.map:
            if c in self._channel_set.keys() and c in self._records.buffers.keys():
                buffers[c] = np.empty(self._records.max_samples, c_int16)
                buckets[c] = np.empty(self._records.max_samples, c_int16)
                handles[c] = buffers[c].ctypes
            else:
                buffers[c] = None
                handles[c] = None
        block_ov = c_int16(0)
        self._records.start = 0
        # wait for data for 1/10 of desired time block
        sleep_time = self._records.interval / 1000 * 0.1 * self._records.max_samples
        try:
            while not self._recording_event.is_set():
                sleep(sleep_time)
                if self._recording_event.is_set():
                    break
                if self._records.autostop and fill_level > self._records.max_samples:
                    self._recording_event.set()
                    ldlib.Stop()
                    break
                block_ov.value = 0
                with self._recording_lock:
                    values = ldlib.GetValues(self._chandle,
                                             handles[self.m.Channels.A], handles[self.m.Channels.B],
                                             handles[self.m.Channels.C], handles[self.m.Channels.D],
                                             byref(block_ov), c_int32(self._records.max_samples))
                    if values > 0:
                        window_ov |= block_ov.value
                        if fill_level + values >= cut_off:
                            left_off = fill_level + values - cut_off
                            if fill_level < cut_off and values - left_off > 0:
                                for c in self._records.buffers.keys():
                                    buckets[c][fill_level:cut_off] = buffers[c][:(values - left_off)]
                            for c in self._records.buffers.keys():
                                self._records.buffers[c]["overflow"] = window_ov & 1 << c > 0
                                if self._records.downsample > 1:
                                    t = buckets[c][:cut_off].reshape(-1, self._records.downsample)
                                    for m in self._records.modes:
                                        if self._records.modes[m] == self.m.RatioModes.agg:
                                            self._records.buffers[c]["min"] = t.min(axis=1)
                                            self._records.buffers[c]["max"] = t.max(axis=1)
                                        elif self._records.modes[m] == self.m.RatioModes.avg:
                                            self._records.buffers[c]["avg"] = t.mean(axis=1)
                                        elif self._records.modes[m] == self.m.RatioModes.dec:
                                            self._records.buffers[c]["dec"] = t[:, 0]
                                else:
                                    self._records.buffers[c]["raw"] = buckets[c][:cut_off]
                            self._records.samples = int(cut_off / self._records.downsample)
                            if self._tape is not None:
                                self._tape.record(self._records)
                            for c in self._records.buffers.keys():
                                if left_off > 0:
                                    buckets[c][:left_off] = buffers[c][(values - left_off):values]
                            fill_level = left_off
                            window_ov = 0
                        else:
                            for c in self._records.buffers.keys():
                                buckets[c][fill_level:(fill_level + values)] = buffers[c][:values]
                            fill_level += values
                            continue
            with self._recording_lock:
                block_ov.value = 0
                values = ldlib.GetValues(self._chandle,
                                         handles[self.m.Channels.A], handles[self.m.Channels.B],
                                         handles[self.m.Channels.C], handles[self.m.Channels.D],
                                         byref(block_ov), c_int32(self._records.max_samples))
                if values > 0 or fill_level > 0:
                    window_ov |= block_ov.value
                    if values > 0 and fill_level + values != cut_off:
                        # discarding values if over block...
                        limit = min(fill_level + values, cut_off)
                        for c in self._records.buffers.keys():
                            buckets[c][fill_level:limit] = buffers[c][:(values - fill_level - limit)]
                        fill_level = limit
                    cut_off = int(fill_level / self._records.downsample) * self._records.downsample
                    for c in self._records.buffers.keys():
                        self._records.buffers[c]["overflow"] = window_ov & 1 << c > 0
                        if self._records.downsample > 1:
                            t = buffers[c][:cut_off].reshape(-1, self._records.downsample)
                            for m in self._records.modes:
                                if self._records.modes[m] == self.m.RatioModes.agg:
                                    self._records.buffers[c]["min"] = t.min(axis=1)
                                    self._records.buffers[c]["max"] = t.max(axis=1)
                                elif self._records.modes[m] == self.m.RatioModes.avg:
                                    self._records.buffers[c]["avg"] = t.mean(axis=1)
                                elif self._records.modes[m] == self.m.RatioModes.dec:
                                    self._records.buffers[c]["dec"] = t[:, 0]
                        else:
                            self._records.buffers[c]["raw"][:] = buckets[c][:fill_level]
                    self._records.samples = int(fill_level / self._records.downsample)
                    if self._tape is not None:
                        self._tape.record(self._records)
        except Exception as ex:
            self.last_error = ex.message
            print "Streaming Worker(%d):" % sys.exc_info()[-1].tb_lineno, self.last_error, type(ex)
        finally:
            with self._recording_lock:
                self._recording_event.clear()

    def _start_fast_streaming(self):
        self._records.interval = 1 if self._records.interval < 1 else int(self._records.interval)
        status = ldlib.RunFastStreaming(self._chandle, c_uint32(self._records.interval), c_int32(self._records.units),
                                        c_uint32(self._records.max_samples * self._records.downsample),
                                        c_int16(self._records.autostop), c_uint32(1),
                                        c_uint32(max(self._records.bufflen * self._records.downsample, 15000)))
        if status == 0:
            return pico_num("PICO_STREAMING_FAILED")
        try:
            self._recording_thread = Thread(target=self._fast_recording_worker, args=(None,))
            if self._recording_event.is_set():
                self._recording_event.clear()
            self._recording_thread.start()
        except Exception as ex:
            if not self._recording_event.is_set():
                self._recording_event.set()
            self.last_error = ex.message
            print "Fast Streaming Start(%d):" % sys.exc_info()[-1].tb_lineno, self.last_error, type(ex)
            return pico_num("PICO_STREAMING_FAILED")

        return pico_num("PICO_OK")

    def _fast_recording_worker(self, *args):
        try:
            self._recording_cb_type = self._streaming_ready()
            self._recording_cb_func = self._recording_cb_type(self._fast_recording_cb)
            sleep_time = (0.01 * self._records.max_samples * self._records.interval * self.m.TimeUnits.multiplier(
                self._records.units, self.m.TimeUnits.s))
            self._recording_buffers = {}
            self._recording_values = 0
            buckets = {}
            cut_off = int(self._records.bufflen / self._records.downsample) * self._records.downsample
            fill_level = 0
            window_ov = 0
            for c in self.m.Channels.map:
                if c in self._channel_set.keys() and c in self._records.buffers.keys():
                    buckets[c] = np.empty(self._records.max_samples, c_int16)
                else:
                    buckets[c] = None
            block_ov = c_int16(0)
            self._records.start = 0
            while not self._recording_event.is_set():
                with self._recording_lock:
                    status = ldlib.GetStreamingLastValues(self._chandle, self._recording_cb_func)
                if status == 0:
                    sleep(sleep_time)
                    continue
                with self._recording_lock:
                    if self._recording_values > 0:
                        do_sleep = False
                        if fill_level + self._recording_values >= cut_off:
                            left_off = fill_level + self._recording_values - cut_off
                            if fill_level < cut_off and self._recording_values - left_off > 0:
                                for c in self._records.buffers.keys():
                                    buckets[c][fill_level:cut_off] = \
                                        self._recording_buffers[c][:(self._recording_values - left_off)]
                            window_ov |= block_ov.value
                            loop = True
                            while loop:
                                for c in self._records.buffers.keys():
                                    self._records.buffers[c]["overflow"] = window_ov & 1 << c > 0
                                    if self._records.downsample > 1:
                                        t = buckets[c][:cut_off].reshape(-1, self._records.downsample)
                                        for m in self._records.modes:
                                            if self._records.modes[m] == self.m.RatioModes.agg:
                                                self._records.buffers[c]["min"] = t.min(axis=1)
                                                self._records.buffers[c]["max"] = t.max(axis=1)
                                            elif self._records.modes[m] == self.m.RatioModes.avg:
                                                self._records.buffers[c]["avg"] = t.mean(axis=1)
                                            elif self._records.modes[m] == self.m.RatioModes.dec:
                                                self._records.buffers[c]["dec"] = t[:, 0]
                                    else:
                                        self._records.buffers[c]["raw"] = buckets[c][:cut_off]
                                self._records.samples = int(cut_off / self._records.downsample)
                                if self._tape is not None:
                                    self._tape.record(self._records)
                                if left_off >= cut_off:
                                    window_ov = block_ov.value
                                    fcut = self._recording_values - left_off
                                    tcut = fcut + cut_off
                                    for c in self._records.buffers.keys():
                                        buckets[c][:cut_off] = self._recording_buffers[c][fcut:tcut]
                                    left_off -= cut_off
                                else:
                                    loop = False
                            for c in self._records.buffers.keys():
                                if left_off > 0:
                                    buckets[c][:left_off] =\
                                        self._recording_buffers[c][
                                        (self._recording_values - left_off):self._recording_values]
                            fill_level = left_off
                            window_ov = 0
                            self._recording_values = 0
                        else:
                            for c in self._records.buffers.keys():
                                buckets[c][fill_level:(fill_level + self._recording_values)] = \
                                    self._recording_buffers[c][:self._recording_values]
                            fill_level += self._recording_values
                            self._recording_values = 0
                    else:
                        do_sleep = True
                if do_sleep and not self._recording_event.is_set():
                    sleep(sleep_time)
            with self._recording_lock:
                if self._recording_values > 0 or fill_level > 0:
                    window_ov |= block_ov.value
                    if self._recording_values > 0 and fill_level + self._recording_values != cut_off:
                        # discarding values if over block...
                        limit = min(fill_level + self._recording_values, cut_off)
                        for c in self._records.buffers.keys():
                            buckets[c][fill_level:limit] =\
                                self._recording_buffers[c][:(self._recording_values - fill_level - limit)]
                        fill_level = limit
                    cut_off = int(fill_level / self._records.downsample) * self._records.downsample
                    for c in self._records.buffers.keys():
                        self._records.buffers[c]["overflow"] = window_ov & 1 << c > 0
                        if self._records.downsample > 1:
                            t = buckets[c][:cut_off].reshape(-1, self._records.downsample)
                            for m in self._records.modes:
                                if self._records.modes[m] == self.m.RatioModes.agg:
                                    self._records.buffers[c]["min"] = t.min(axis=1)
                                    self._records.buffers[c]["max"] = t.max(axis=1)
                                elif self._records.modes[m] == self.m.RatioModes.avg:
                                    self._records.buffers[c]["avg"] = t.mean(axis=1)
                                elif self._records.modes[m] == self.m.RatioModes.dec:
                                    self._records.buffers[c]["dec"] = t[:, 0]
                        else:
                            self._records.buffers[c]["raw"] = buckets[c][:fill_level]
                    self._records.samples = int(fill_level / self._records.downsample)
                    if self._tape is not None:
                        self._tape.record(self._records)

        except Exception as ex:
            self.last_error = ex.message
            print "Streaming Worker(%d):" % sys.exc_info()[-1].tb_lineno, self.last_error, type(ex)
        finally:
            with self._recording_lock:
                self._recording_event.clear()

    def _fast_recording_cb(self, ref_buffers, overflow, trigger_at, triggered, auto_stop, values):
        if auto_stop > 0:
            self._recording_event.set()
            self._records.final = True
            return
        if values > 0:
            buffers = cast(ref_buffers, POINTER(c_void_p))
            for c in self._records.buffers.keys():
                self._recording_buffers[c] =\
                    np.copy(np.ctypeslib.as_array(cast(buffers[2 * c], POINTER(c_int16)), shape=(values, )))
            self._recording_values = values
            self._recording_overflow = overflow
            self._recording_triggered = triggered
            self._recording_trigger_at = trigger_at
        else:
            self._recording_values = 0

    @staticmethod
    def _streaming_ready():
        if sys.platform == "win32":
            return WINFUNCTYPE(None, c_void_p, c_int16, c_uint32, c_int16, c_int16, c_uint32)
        else:
            return CFUNCTYPE(None, c_void_p, c_int16, c_uint32, c_int16, c_int16, c_uint32)

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
        status = ldlib.Stop(self._chandle)
        if status == 0:
            return pico_num("PICO_INVALID_HANDLE")
        else:
            pico_num("PICO_OK")

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
        return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE"), None

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
        if mode not in (None, self.m.IndexModes.single):
            return pico_num("PICO_INVALID_BUFFER")

        wave = np.array([self.info.awg_min if v < self.info.awg_min else
                         (self.info.awg_max if v > self.info.awg_max else v)
                         for v in waveform], dtype=c_uint8)
        l = min(len(wave), self.info.awg_size)
        # 89.4784853333 = 2^32 / 48000000
        phase = int(89.4784853333 * frequency * self.info.awg_size / l)
        status = ldlib.SetSigGenArbitrary(self._chandle, c_int32(offset), c_uint32(pk2pk),
                                          c_uint32(phase), c_uint32(phase), c_uint32(0), c_uint32(0),
                                          wave.ctypes, c_int32(l), c_int32(self.m.SweepTypes.up), c_uint32(0))
        if status > 0:
            return pico_num("PICO_OK")
        return pico_num("PICO_SIG_GEN_PARAM")

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

        if not self.info.has_adv_trigger or digital is not None:
            return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")

        conditions = conditions if conditions is not None else ()
        analog = analog if analog is not None else ()

        if not isinstance(conditions, (tuple, list)):
            return pico_num("PICO_INVALID_CONDITION_INFO")
        if not isinstance(analog, (tuple, list)):
            return pico_num("PICO_INVALID_TRIGGER_PROPERTY")
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

        status = ldlib.SetAdvTriggerChannelDirections(
            self._chandle,
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.A]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.B]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.C]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.D]]),
            c_int32(analogdir[self.m.TriggerChannels.labels[self.m.TriggerChannels.Ext]])
        )
        if status == 0:
            return pico_num("PICO_INVALID_TRIGGER_PROPERTY")

        status = \
            ldlib.SetAdvTriggerChannelProperties(self._chandle, analogprops, c_int16(len(analogout)), c_int32(waitfor))
        if status == 0:
            return pico_num("PICO_INVALID_TRIGGER_PROPERTY")

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

        status = ldlib.SetAdvTriggerChannelConditions(self._chandle, conds, c_int16(len(conditionsout)))
        if status == 0:
            return pico_num("PICO_INVALID_TRIGGER_PROPERTY")

        status = ldlib.SetAdvTriggerDelay(self._chandle, c_uint32(0), c_float(-100.0 * self.trigg_ratio))
        if status == 0:
            return pico_num("PICO_INVALID_PARAMETER")

        self.trigger_conditions = conditionsout
        self.trigger_analog = analogout
        self.trigger_digital = None
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

        return TriggerChannelProperties(
            channel=channel,
            threshUpperADC=int((upperbound * 1.0 - int(upperbound * 0.999999)) * self.info.max_adc),
            threshLowerADC=int((lowerbound * 1.0 - int(lowerbound * 0.999999)) * self.info.max_adc),
            hysteresis=int((abs(float(lowerhys)) % 1) * 2 * self.info.max_adc),
            threshMode=mode, direction=direction)

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
        if status == 0:
            return pico_num("PICO_PULSE_WIDTH_QUALIFIER")

        self.pwq_conditions = condout
        self.pwq_direction = direction
        self.pwq_lower = lower
        self.pwq_upper = upper
        self.pwq_type = pwqtype
        return pico_num("PICO_OK")

    def is_trigger_set(self):
        """ Checks whether trigger is set for the next collection
        :returns: result of the check
        :rtype: bool
        """
        if self._handle <= 0:
            return None
        return self.trigger or (self.info.has_adv_trigger and (True in [c.is_set() for c in self.trigger_conditions]))

    def get_trigger_time_offset(self, segment):
        """ Returns time offset in nanoseconds that occurred in the specified segment
        :param segment: memory segment number
        :type segment: int
        :returns: status of the call, offset
        :rtype: tuple(int, float)
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")

    def stop(self):
        """
        Stops any pending activities on the device
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        for e in (self._collect_event, self._recording_event, self._async_event):
            if e is not None and e.is_set():
                e.set()
        status = ldlib.Stop(self._chandle)
        if status == 0:
            return pico_num("PICO_INVALID_HANDLE")
        return pico_num("PICO_OK")

    def close_unit(self):
        """ Closes currently open unit
        :returns: status of the call
        :rtype: int
        """
        if self._handle > 0:
            self.stop()
            self.release_all_buffers()
            status = ldlib.CloseUnit(self._chandle)
            if status == 0:
                return pico_num("PICO_INVALID_HANDLE")
            self._handle = 0
            self._chandle.value = 0
            return pico_num("PICO_OK")
        else:
            return pico_num("PICO_INVALID_HANDLE")

    def _get_timebase(self, timebase, samples, ref_interval, oversample, ref_maxsamples, segment):
        status = ldlib.GetTimebase(self._chandle, c_int16(timebase), c_int32(samples), ref_interval, None,
                                   c_int16(oversample), ref_maxsamples)
        if status != 0:
            return pico_num("PICO_OK")
        return pico_num("PICO_INVALID_SAMPLE")

    def _set_sig_gen_built_in(self, offset, pk2pk, wave, start, stop, increment, dwelltime,
                              sweep, extra, shots, sweeps, trigt, trigs, threshold):

        status = ldlib.SetSigGenBuiltIn(self._chandle, c_int32(offset), c_uint32(pk2pk), c_int32(wave),
                                        c_float(start), c_float(stop), c_float(increment), c_float(dwelltime),
                                        c_int32(sweep), c_uint32(sweeps))
        if status == 0:
            return pico_num("PICO_SIG_GEN_PARAM")
        return pico_num("PICO_OK")

    def ping_unit(self):
        """ Checks if current device is alive
        :returns: status PICO_OK if alive
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        status = ldlib.PingUnit(self._chandle)
        if status == 0:
            return pico_num("PICO_NOT_RESPONDING")
        return pico_num("PICO_OK")


def enumerate_units(loaded_lib):
    """ Module function for enumerating all devices served by this driver
    :param loaded_lib: dict2class object of loaded library bindings
    :type loaded_lib: dict2class
    :returns: list of serials of found devices
    :rtype: list, tuple
    """
    serials = ()
    handles = ()
    while True:
        try:
            handle = loaded_lib.OpenUnit()
        except AttributeError:
            print "Library not loaded"
            return ()
        if handle > 0:
            handles += (handle, )
        else:
            break
    for handle in handles:
        info = create_string_buffer("\0", MAX_INFO_LEN)
        info_len = loaded_lib.GetUnitInfo(c_int16(handle), info, c_int16(MAX_INFO_LEN), c_int16(Info.batch_and_serial))
        if info_len > 0:
            serials += (info.value[:info_len], )
        loaded_lib.CloseUnit(c_int16(handle))
    return serials
