#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps3000.h C header file
for PicoScope 3000 Series oscilloscopes using the ps3000 driver API functions.
"""

from ps3000base import *
from picosdk import ps3000base

name = "ps3000"
_libps3000 = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps3000
ldlib.name = name

""" int16_t ps3000_open_unit
    (
        void
    ); """
make_symbol(ldlib, "OpenUnit", "ps3000_open_unit", c_int16, None)

""" int16_t ps3000_get_unit_info
    (
        int16_t  handle,
        int8_t  *string,
        int16_t  string_length,
        int16_t  line
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps3000_get_unit_info", c_int16, [c_int16, c_char_p, c_int16, c_int16])

""" int16_t ps3000_flash_led
    (
        int16_t handle
    ); """
make_symbol(ldlib, "FlashLed", "ps3000_flash_led", c_int16, [c_int16, ])

""" int16_t ps3000_close_unit
    (
        int16_t handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps3000_close_unit", c_int16, [c_int16, ])

""" int16_t ps3000_set_channel
    (
        int16_t  handle,
        int16_t  channel,
        int16_t  enabled,
        int16_t  dc,
        int16_t  range
    ); """
make_symbol(ldlib, "SetChannel", "ps3000_set_channel", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16])

""" int16_t ps3000_get_timebase
    (
        int16_t  handle,
        int16_t  timebase,
        int32_t  no_of_samples,
        int32_t *time_interval,
        int16_t *time_units,
        int16_t  oversample,
        int32_t *max_samples
    ); """
make_symbol(ldlib, "GetTimebase", "ps3000_get_timebase", c_int16,
            [c_int16, c_int16, c_int32, c_void_p, c_void_p, c_int16, c_void_p])

""" int32_t ps3000_set_siggen
    (
        int16_t  handle,
        int16_t  wave_type,
        int32_t  start_frequency,
        int32_t  stop_frequency,
        float    increment,
        int16_t  dwell_time,
        int16_t  repeat,
        int16_t  dual_slope
    ); """
make_symbol(ldlib, "SetSiggen", "ps3000_set_siggen", c_int32,
            [c_int16, c_int16, c_int32, c_int32, c_float, c_int16, c_int16, c_int16])

""" int32_t ps3000_set_ets
    (
        int16_t  handle,
        int16_t  mode,
        int16_t  ets_cycles,
        int16_t  ets_interleave
    ); """
make_symbol(ldlib, "SetEts", "ps3000_set_ets", c_int32, [c_int16, c_int16, c_int16, c_int16])

""" int16_t ps3000_set_trigger
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        int16_t  delay,
        int16_t  auto_trigger_ms
    ); """
make_symbol(ldlib, "SetTrigger0", "ps3000_set_trigger", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16, c_int16])

""" int16_t ps3000_set_trigger2
    (
        int16_t  handle,
        int16_t  source,
        int16_t  threshold,
        int16_t  direction,
        float    delay,
        int16_t  auto_trigger_ms
    ); """
make_symbol(ldlib, "SetTrigger", "ps3000_set_trigger2", c_int16, [c_int16, c_int16, c_int16, c_int16, c_float, c_int16])

""" int16_t ps3000_run_block
    (
        int16_t handle,
        int32_t  no_of_values,
        int16_t  timebase,
        int16_t  oversample,
        int32_t * time_indisposed_ms
    ); """
make_symbol(ldlib, "RunBlock", "ps3000_run_block", c_int16, [c_int16, c_int32, c_int16, c_int16, c_void_p])


""" int16_t ps3000_run_streaming
    (
        int16_t  handle,
        int16_t  sample_interval_ms,
        int32_t  max_samples,
        int16_t  windowed
    ); """
make_symbol(ldlib, "RunCompatibleStreaming", "ps3000_run_streaming", c_int16, [c_int16, c_int16, c_int32, c_int16])

""" int16_t ps3000_run_streaming_ns
    (
        int16_t            handle,
        uint32_t           sample_interval,
        PS3000_TIME_UNITS  time_units,
        uint32_t           max_samples,
        int16_t            auto_stop,
        uint32_t           noOfSamplesPerAggregate,
        uint32_t           overview_buffer_size
    ); """
make_symbol(ldlib, "RunFastStreaming", "ps3000_run_streaming_ns", c_int16,
            [c_int16, c_uint32, c_int32, c_uint32, c_int16, c_uint32, c_uint32])


""" int16_t ps3000_ready
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Ready", "ps3000_ready", c_int16, [c_int16, ])

""" int16_t ps3000_stop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps3000_stop", c_int16, [c_int16, ])

""" int32_t ps3000_get_values
    (
        int16_t  handle,
        int16_t *buffer_a,
        int16_t *buffer_b,
        int16_t *buffer_c,
        int16_t *buffer_d,
        int16_t *overflow,
        int32_t  no_of_values
    ); """
make_symbol(ldlib, "GetValues", "ps3000_get_values", c_int32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int32])

""" void ps3000_release_stream_buffer
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "ReleaseStreamBuffer", "ps3000_release_stream_buffer", None, [c_int16, ])

""" int32_t ps3000_get_times_and_values
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
make_symbol(ldlib, "GetTimesAndValues", "ps3000_get_times_and_values", c_int32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_int16, c_int32])

""" int16_t ps3000_open_unit_async
    (
        void
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps3000_open_unit_async", c_int16, None)

""" int16_t ps3000_open_unit_progress
    (
        int16_t *handle,
        int16_t *progress_percent
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps3000_open_unit_progress", c_int16, [c_void_p, c_void_p])

""" int16_t ps3000_streaming_ns_get_interval_stateless
    (
        int16_t   handle,
        int16_t   nChannels,
        uint32_t *sample_interval
    ); """
make_symbol(ldlib, "GetStreamingInterval", "ps3000_streaming_ns_get_interval_stateless", c_int16,
            [c_int16, c_int16, c_void_p])

""" int16_t ps3000_get_streaming_last_values
    (
        int16_t  handle,
        GetOverviewBuffersMaxMin
    ); """
make_symbol(ldlib, "GetStreamingLastValues", "ps3000_get_streaming_last_values", c_int16, [c_int16, c_void_p])

""" int16_t ps3000_overview_buffer_status
    (
        int16_t  handle,
        int16_t *previous_buffer_overrun
    ); """
make_symbol(ldlib, "OverviewBufferStatus", "ps3000_overview_buffer_status", c_int16, [c_int16, c_void_p])

""" uint32_t ps3000_get_streaming_values
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
make_symbol(ldlib, "GetStreamingValues", "ps3000_get_streaming_values", c_uint32,
            [c_int16, c_void_p,
             c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p,
             c_void_p, c_void_p, c_void_p, c_uint32, c_uint32])

""" uint32_t ps3000_get_streaming_values_no_aggregation
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
make_symbol(ldlib, "GetStreamingRawValues", "ps3000_get_streaming_values_no_aggregation", c_uint32,
            [c_int16, c_void_p,
             c_void_p, c_void_p, c_void_p, c_void_p,
             c_void_p, c_void_p, c_void_p, c_uint32])

""" int16_t ps3000_save_streaming_data
    (
        int16_t               handle,
        PS3000_CALLBACK_FUNC  lpCallbackFunc,
        int16_t              *dataBuffers,
        int16_t               dataBufferSize
    ); """
make_symbol(ldlib, "SaveStreamingData", "ps3000_save_streaming_data", c_int16, [c_int16, c_void_p, c_void_p, c_int16])

""" int16_t ps3000SetAdvTriggerChannelProperties
    (
        int16_t                            handle,
        PS3000_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                            nChannelProperties,
        int32_t                            autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetAdvTriggerChannelProperties", "ps3000SetAdvTriggerChannelProperties", c_int16,
            [c_int16, c_void_p, c_int16, c_int32])

""" int16_t ps3000SetAdvTriggerChannelConditions
    (
        int16_t                    handle,
        PS3000_TRIGGER_CONDITIONS *conditions,
        int16_t                    nConditions
    ); """
make_symbol(ldlib, "SetAdvTriggerChannelConditions", "ps3000SetAdvTriggerChannelConditions", c_int16,
            [c_int16, c_void_p, c_int16])

""" int16_t ps3000SetAdvTriggerChannelDirections
    (
        int16_t                     handle,
        PS3000_THRESHOLD_DIRECTION  channelA,
        PS3000_THRESHOLD_DIRECTION  channelB,
        PS3000_THRESHOLD_DIRECTION  channelC,
        PS3000_THRESHOLD_DIRECTION  channelD,
        PS3000_THRESHOLD_DIRECTION  ext
    ); """
make_symbol(ldlib, "SetAdvTriggerChannelDirections", "ps3000SetAdvTriggerChannelDirections", c_int16,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32])

""" int16_t ps3000SetPulseWidthQualifier
    (
        int16_t                     handle,
        PS3000_PWQ_CONDITIONS      *conditions,
        int16_t                     nConditions,
        PS3000_THRESHOLD_DIRECTION  direction,
        uint32_t                    lower,
        uint32_t                    upper,
        PS3000_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifier", "ps3000SetPulseWidthQualifier", c_int16,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" int16_t ps3000SetAdvTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay,
        float     preTriggerDelay
    ); """
make_symbol(ldlib, "SetAdvTriggerDelay", "ps3000SetAdvTriggerDelay", c_int16, [c_int16, c_uint32, c_float])

""" int16_t ps3000PingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps3000PingUnit", c_int16, [c_int16, ])


variants = ("3204", "3205", "3206", "3224", "3424", "3425")


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
        self.info.has_adv_trigger = False
        self.info.has_fast_streaming = True
        self.info.has_awg = False
        self.info.has_siggen = False
        if self.info.variant_info == "3204":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r100mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.memory = 256000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "3205":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r100mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.memory = 512000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "3206":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r100mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.memory = 1024000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "3224":
            self.info.num_channels = 2
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.memory = 512000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "3424":
            self.info.num_channels = 4
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.memory = 512000
            self.info.memps = self.info.memory
        elif self.info.variant_info == "3425":
            self.info.num_channels = 4
            self.info.min_range = self.m.Ranges.r100mv
            self.info.max_range = self.m.Ranges.r400v
            self.info.memory = 512000
            self.info.memps = self.info.memory
        else:
            return pico_num("PICO_INFO_UNAVAILABLE")
        return pico_num("PICO_OK")


def enumerate_units():
    global ldlib
    return ps3000base.enumerate_units(ldlib)
