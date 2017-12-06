#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps2000.h C header file
for PicoScope 2000 Series oscilloscopes using the ps2000 driver API functions.
"""

from ps3000base import *
from picosdk import ps3000base

name = "ps2000"
_libps2000 = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps2000
ldlib.name = name

""" int16_t ps2000_open_unit
    (
        void
    ); """
make_symbol(ldlib, "OpenUnit", "ps2000_open_unit", c_int16, None)

""" int16_t ps2000_get_unit_info
    (
        int16_t  handle,
        int8_t  *string,
        int16_t  string_length,
        int16_t  line
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps2000_get_unit_info", c_int16, [c_int16, c_char_p, c_int16, c_int16])

""" int16_t ps2000_flash_led
    (
        int16_t handle
    ); """
make_symbol(ldlib, "FlashLed", "ps2000_flash_led", c_int16, [c_int16, ])

""" int16_t ps2000_close_unit
    (
        int16_t handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps2000_close_unit", c_int16, [c_int16, ])

""" int16_t ps2000_set_channel
    (
        int16_t  handle,
        int16_t  channel,
        int16_t  enabled,
        int16_t  dc,
        int16_t  range
    ); """
make_symbol(ldlib, "SetChannel", "ps2000_set_channel", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16])

""" int16_t ps2000_get_timebase
    (
        int16_t  handle,
        int16_t  timebase,
        int32_t  no_of_samples,
        int32_t *time_interval,
        int16_t *time_units,
        int16_t  oversample,
        int32_t *max_samples
    ); """
make_symbol(ldlib, "GetTimebase", "ps2000_get_timebase", c_int16,
            [c_int16, c_int16, c_int32, c_void_p, c_void_p, c_int16, c_void_p])

""" int16_t ps2000_set_trigger
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        int16_t  delay,
        int16_t  auto_trigger_ms
    ); """
make_symbol(ldlib, "SetTrigger0", "ps2000_set_trigger", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16, c_int16])

""" int16_t ps2000_set_trigger2
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        float    delay,
        int16_t  auto_trigger_ms
    ); """
make_symbol(ldlib, "SetTrigger", "ps2000_set_trigger2", c_int16, [c_int16, c_int16, c_int16, c_int16, c_float, c_int16])

""" int16_t ps2000_run_block
    (
        int16_t handle,
        int32_t  no_of_values,
        int16_t  timebase,
        int16_t  oversample,
        int32_t * time_indisposed_ms
    ); """
make_symbol(ldlib, "RunBlock", "ps2000_run_block", c_int16, [c_int16, c_int32, c_int16, c_int16, c_void_p])

""" int16_t ps2000_run_streaming
    (
        int16_t  handle,
        int16_t  sample_interval_ms,
        int32_t  max_samples,
        int16_t  windowed
    ); """
make_symbol(ldlib, "RunCompatibleStreaming", "ps2000_run_streaming", c_int16, [c_int16, c_int16, c_int32, c_int16])

""" int16_t ps2000_run_streaming_ns
    (
        int16_t            handle,
        uint32_t           sample_interval,
        PS2000_TIME_UNITS  time_units,
        uint32_t           max_samples,
        int16_t            auto_stop,
        uint32_t           noOfSamplesPerAggregate,
        uint32_t           overview_buffer_size
    ); """
make_symbol(ldlib, "RunFastStreaming", "ps2000_run_streaming_ns", c_int16,
            [c_int16, c_uint32, c_int32, c_uint32, c_int16, c_uint32, c_uint32])

""" int16_t ps2000_ready
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Ready", "ps2000_ready", c_int16, [c_int16, ])

""" int16_t ps2000_stop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps2000_stop", c_int16, [c_int16, ])

""" int32_t ps2000_get_values
    (
        int16_t  handle,
        int16_t *buffer_a,
        int16_t *buffer_b,
        int16_t *buffer_c,
        int16_t *buffer_d,
        int16_t *overflow,
        int32_t  no_of_values
    ); """
make_symbol(ldlib, "GetValues", "ps2000_get_values", c_int32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int32])

""" int32_t ps2000_get_times_and_values
    (
        int16_t  handle,
        int32_t *times,
        int16_t *buffer_a,
        int16_t *buffer_b,
        int16_t *buffer_c,
        int16_t *buffer_d,
        int16_t *overflow,
        int16_t  time_units,
        int32_t  no_of_values
    ); """
make_symbol(ldlib, "GetTimesAndValues", "ps2000_get_times_and_values", c_int32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int16, c_int32])

""" int16_t ps2000_last_button_press
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "LastButtonPress", "ps2000_last_button_press", c_int16, [c_int16, ])

""" int32_t ps2000_set_ets
    (
        int16_t  handle,
        int16_t  mode,
        int16_t  ets_cycles,
        int16_t  ets_interleave
    ); """
make_symbol(ldlib, "SetEts", "ps2000_set_ets", c_int32, [c_int16, c_int16, c_int16, c_int16])

""" int16_t ps2000_set_led
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "SetLed", "ps2000_set_led", c_int16, [c_int16, c_int16])

""" int16_t ps2000_open_unit_async
    (
        void
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps2000_open_unit_async", c_int16, None)

""" int16_t ps2000_open_unit_progress
    (
        int16_t *handle,
        int16_t *progress_percent
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps2000_open_unit_progress", c_int16, [c_void_p, c_void_p])

""" int16_t ps2000_get_streaming_last_values
    (
        int16_t  handle,
        GetOverviewBuffersMaxMin
    ); """
make_symbol(ldlib, "GetStreamingLastValues", "ps2000_get_streaming_last_values", c_int16, [c_int16, c_void_p])

""" int16_t ps2000_overview_buffer_status
    (
        int16_t  handle,
        int16_t *previous_buffer_overrun
    ); """
make_symbol(ldlib, "OverviewBufferStatus", "ps2000_overview_buffer_status", c_int16, [c_int16, c_void_p])

""" uint32_t ps2000_get_streaming_values
    (
        int16_t  handle,
        double   *start_time,
        int16_t  *pbuffer_a_max,
        int16_t  *pbuffer_a_min,
        int16_t  *pbuffer_b_max,
        int16_t  *pbuffer_b_min,
        int16_t  *pbuffer_c_max,
        int16_t  *pbuffer_c_min,
        int16_t  *pbuffer_d_max,
        int16_t  *pbuffer_d_min,
        int16_t  *overflow,
        uint32_t *triggerAt,
        int16_t  *triggered,
        uint32_t  no_of_values,
        uint32_t  noOfSamplesPerAggregate
    ); """
make_symbol(ldlib, "GetStreamingValues", "ps2000_get_streaming_values", c_uint32,
            [c_int16, c_void_p,
             c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p,
             c_void_p, c_void_p, c_void_p, c_uint32, c_uint32])

""" uint32_t ps2000_get_streaming_values_no_aggregation
    (
        int16_t handle,
        double *start_time,
        int16_t * pbuffer_a,
        int16_t * pbuffer_b,
        int16_t * pbuffer_c,
        int16_t * pbuffer_d,
        int16_t * overflow,
        uint32_t * triggerAt,
        int16_t * trigger,
        uint32_t no_of_values
    ); """
make_symbol(ldlib, "GetStreamingRawValues", "ps2000_get_streaming_values_no_aggregation", c_uint32,
            [c_int16, c_void_p,
             c_void_p, c_void_p, c_void_p, c_void_p,
             c_void_p, c_void_p, c_void_p, c_uint32])

""" int16_t ps2000_set_light
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "SetLight", "ps2000_set_light", c_int16, [c_int16, c_int16])

""" int16_t ps2000_set_sig_gen_arbitrary
    (
        int16_t            handle,
        int32_t            offsetVoltage,
        uint32_t           pkToPk,
        uint32_t           startDeltaPhase,
        uint32_t           stopDeltaPhase,
        uint32_t           deltaPhaseIncrement,
        uint32_t           dwellCount,
        uint8_t           *arbitraryWaveform,
        int32_t            arbitraryWaveformSize,
        PS2000_SWEEP_TYPE  sweepType,
        uint32_t           sweeps
    ); """
make_symbol(ldlib, "SetSigGenArbitrary", "ps2000_set_sig_gen_arbitrary", c_int16,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32, c_uint32])

""" int16_t ps2000_set_sig_gen_built_in
    (
        int16_t            handle,
        int32_t            offsetVoltage,
        uint32_t           pkToPk,
        PS2000_WAVE_TYPE   waveType,
        float              startFrequency,
        float              stopFrequency,
        float              increment,
        float              dwellTime,
        PS2000_SWEEP_TYPE  sweepType,
        uint32_t           sweeps
    ); """
make_symbol(ldlib, "SetSigGenBuiltIn", "ps2000_set_sig_gen_built_in", c_int16,
            [c_int16, c_int32, c_uint32, c_int32, c_float, c_float, c_float, c_float, c_int32, c_uint32])

""" int16_t ps2000SetAdvTriggerChannelProperties
    (
        int16_t                            handle,
        PS2000_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                            nChannelProperties,
        int32_t                            autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetAdvTriggerChannelProperties", "ps2000SetAdvTriggerChannelProperties", c_int16,
            [c_int16, c_void_p, c_int16, c_int32])

""" int16_t ps2000SetAdvTriggerChannelConditions
    (
        int16_t                    handle,
        PS2000_TRIGGER_CONDITIONS *conditions,
        int16_t                    nConditions
    ); """
make_symbol(ldlib, "SetAdvTriggerChannelConditions", "ps2000SetAdvTriggerChannelConditions", c_int16,
            [c_int16, c_void_p, c_int16])

""" int16_t ps2000SetAdvTriggerChannelDirections
    (
        int16_t                     handle,
        PS2000_THRESHOLD_DIRECTION  channelA,
        PS2000_THRESHOLD_DIRECTION  channelB,
        PS2000_THRESHOLD_DIRECTION  channelC,
        PS2000_THRESHOLD_DIRECTION  channelD,
        PS2000_THRESHOLD_DIRECTION  ext
    ); """
make_symbol(ldlib, "SetAdvTriggerChannelDirections", "ps2000SetAdvTriggerChannelDirections", c_int16,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32])

""" int16_t ps2000SetPulseWidthQualifier
    (
        int16_t                     handle,
        PS2000_PWQ_CONDITIONS      *conditions,
        int16_t                     nConditions,
        PS2000_THRESHOLD_DIRECTION  direction,
        uint32_t                    lower,
        uint32_t                    upper,
        PS2000_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifier", "ps2000SetPulseWidthQualifier", c_int16,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" int16_t ps2000SetAdvTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay,
        float     preTriggerDelay
    ); """
make_symbol(ldlib, "SetAdvTriggerDelay", "ps2000SetAdvTriggerDelay", c_int16, [c_int16, c_uint32, c_float])

""" int16_t ps2000PingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps2000PingUnit", c_int16, [c_int16, ])

variants = ("2104", "2105", "2202", "2203", "2204", "2205", "2204A", "2205A")


class Device(ps3000base.PS3000Device):
    def __init__(self):
        self.m = sys.modules[__name__]
        super(Device, self).__init__(ldlib)

    def _set_variant_info(self):
        """ Sets device variant specific properties
        :returns: status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if not hasattr(self.info, "variant_info") or self.info.variant_info is None:
            return pico_num("PICO_INFO_UNAVAILABLE")
        self.info.num_ports = 0
        self.info.max_segments = 32
        if self.info.variant_info == "2104":
            self.info.num_channels = 1
            self.info.min_range = self.m.Ranges.r100mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_adv_trigger = False
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.has_fast_streaming = False
            self.info.memory = 8000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "2105":
            self.info.num_channels = 1
            self.info.min_range = self.m.Ranges.r100mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_adv_trigger = False
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.has_fast_streaming = False
            self.info.memory = 24000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "2202":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r100mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_adv_trigger = False
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.has_fast_streaming = False
            self.info.memory = 32000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "2203":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_adv_trigger = True
            self.info.has_siggen = True
            self.info.siggen_frequency = 100000
            self.info.siggen_min = 0
            self.info.siggen_max = 40000000
            self.info.has_awg = True
            self.info.awg_size = 4096
            self.info.has_fast_streaming = True
            self.info.memory = 8000
            self.info.memps = self.info.memory
        elif self.info.variant_info[:4] == "2204":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_adv_trigger = True
            self.info.has_siggen = True
            self.info.siggen_frequency = 100000
            self.info.siggen_min = 0
            self.info.siggen_max = 40000000
            self.info.has_awg = True
            self.info.awg_size = 4096
            self.info.has_fast_streaming = True
            self.info.memory = 8000
            self.info.memps = self.info.memory
        elif self.info.variant_info[:4] == "2205":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_adv_trigger = True
            self.info.has_siggen = True
            self.info.siggen_frequency = 100000
            self.info.siggen_min = 0
            self.info.siggen_max = 40000000
            self.info.has_awg = True
            self.info.awg_size = 4096
            self.info.has_fast_streaming = True
            self.info.memory = 16000
            self.info.memps = self.info.memory
        else:
            return pico_num("PICO_INFO_UNAVAILABLE")
        return pico_num("PICO_OK")


def enumerate_units():
    global ldlib
    return ps3000base.enumerate_units(ldlib)
