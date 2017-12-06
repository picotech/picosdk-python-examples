#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps4000Api.h C header
file for PicoScope 4000 Series oscilloscopes using the ps4000 driver API
functions.
"""

from picosdk.ps5000base import *
from psutils import *
from picosdk import ps5000base

name = "ps4000"
_libps4000 = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps4000
ldlib.name = name

""" PICO_STATUS ps4000OpenUnit
    (
        int16_t *handle
    ); """
make_symbol(ldlib, "OpenUnit0", "ps4000OpenUnit", c_uint32, [c_void_p, ])

""" PICO_STATUS ps4000OpenUnitAsync
    (
        int16_t *status
    ); """
make_symbol(ldlib, "OpenUnitAsync0", "ps4000OpenUnitAsync", c_uint32, [c_void_p])

""" PICO_STATUS ps4000OpenUnitEx
    (
        int16_t *handle,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnit", "ps4000OpenUnitEx", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps4000OpenUnitAsyncEx
    (
        int16_t *status,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps4000OpenUnitAsync", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps4000OpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps4000OpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps4000GetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t   *requiredSize,
        PICO_INFO  info
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps4000GetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps4000FlashLed
    (
        int16_t  handle,
        int16_t  start
    ); """
make_symbol(ldlib, "FlashLed", "ps4000FlashLed", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps4000IsLedFlashing
    (
        int16_t  handle,
        int16_t *status
    ); """
make_symbol(ldlib, "IsLedFlashing", "ps4000IsLedFlashing", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000CloseUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps4000CloseUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000MemorySegments
    (
        int16_t   handle,
        uint16_t  nSegments,
        int32_t  *nMaxSamples
    ); """
make_symbol(ldlib, "MemorySegments", "ps4000MemorySegments", c_uint32, [c_int16, c_uint16, c_void_p])

""" PICO_STATUS ps4000SetChannel
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t         enabled,
        int16_t         dc,
        PS4000_RANGE    range
    ); """
make_symbol(ldlib, "SetChannel", "ps4000SetChannel", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_int32])

""" PICO_STATUS ps4000SetNoOfCaptures
    (
        int16_t   handle,
        uint16_t  nCaptures
    ); """
make_symbol(ldlib, "SetNoOfCaptures", "ps4000SetNoOfCaptures", c_uint32, [c_int16, c_uint16])

""" PICO_STATUS ps4000GetTimebase
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        int32_t  *timeIntervalNanoseconds,
        int16_t   oversample,
        int32_t  *maxSamples,
        uint16_t  segmentIndex
    ); """
make_symbol(ldlib, "GetTimebase0", "ps4000GetTimebase", c_uint32,
            [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint16])

""" PICO_STATUS ps4000GetTimebase2
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        float    *timeIntervalNanoseconds,
        int16_t   oversample,
        int32_t  *maxSamples,
        uint16_t  segmentIndex
    ); """
make_symbol(ldlib, "GetTimebase", "ps4000GetTimebase2", c_uint32,
            [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint16])

""" PICO_STATUS ps4000SigGenOff
    (
        int16_t handle
    ); """
make_symbol(ldlib, "SigGenOff", "ps4000SigGenOff", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000SetSigGenArbitrary
    (
        int16_t             handle,
        int32_t             offsetVoltage,
        uint32_t            pkToPk,
        uint32_t            startDeltaPhase,
        uint32_t            stopDeltaPhase,
        uint32_t            deltaPhaseIncrement,
        uint32_t            dwellCount,
        int16_t            *arbitraryWaveform,
        int32_t             arbitraryWaveformSize,
        SWEEP_TYPE          sweepType,
        int16_t             operationType,
        INDEX_MODE          indexMode,
        uint32_t            shots,
        uint32_t            sweeps,
        SIGGEN_TRIG_TYPE    triggerType,
        SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t             extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenArbitrary", "ps4000SetSigGenArbitrary", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p,
             c_int32, c_int32, c_int16, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps4000SetSigGenBuiltIn
    (
        int16_t             handle,
        int32_t             offsetVoltage,
        uint32_t            pkToPk,
        int16_t             waveType,
        float               startFrequency,
        float               stopFrequency,
        float               increment,
        float               dwellTime,
        SWEEP_TYPE          sweepType,
        int16_t             operationType,
        uint32_t            shots,
        uint32_t            sweeps,
        SIGGEN_TRIG_TYPE    triggerType,
        SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t             extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenBuiltIn", "ps4000SetSigGenBuiltIn", c_uint32,
            [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float,
             c_int32, c_int16, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps4000SigGenFrequencyToPhase
    (
        int16_t     handle,
        double      frequency,
        INDEX_MODE  indexMode,
        uint32_t    bufferLength,
        uint32_t   *phase
    ); """
make_symbol(ldlib, "SigGenFrequencyToPhase", "ps4000SigGenFrequencyToPhase", c_uint32,
            [c_int16, c_double, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps4000SigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
make_symbol(ldlib, "SigGenArbitraryMinMaxValues", "ps4000SigGenArbitraryMinMaxValues", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps4000SigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "SigGenSoftwareControl", "ps4000SigGenSoftwareControl", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps4000SetEts
    (
        int16_t          handle,
        PS4000_ETS_MODE  mode,
        int16_t          etsCycles,
        int16_t          etsInterleave,
        int32_t         *sampleTimePicoseconds
    ); """
make_symbol(ldlib, "SetEts", "ps4000SetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

""" PICO_STATUS ps4000SetSimpleTrigger
    (
        int16_t              handle,
        int16_t              enable,
        PS4000_CHANNEL       source,
        int16_t              threshold,
        THRESHOLD_DIRECTION  direction,
        uint32_t             delay,
        int16_t              autoTrigger_ms
    ); """
make_symbol(ldlib, "SetSimpleTrigger", "ps4000SetSimpleTrigger", c_uint32,
            [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

""" PICO_STATUS ps4000SetTriggerChannelProperties
    (
        int16_t                     handle,
        TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                     nChannelProperties,
        int16_t                     auxOutputEnable,
        int32_t                     autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetTriggerChannelProperties", "ps4000SetTriggerChannelProperties", c_uint32,
            [c_int16, c_void_p, c_int16, c_int16, c_int32])

""" PICO_STATUS ps4000SetExtTriggerRange
    (
        int16_t       handle,
        PS4000_RANGE  extRange
    ); """
make_symbol(ldlib, "SetExtTriggerRange", "ps4000SetExtTriggerRange", c_uint32, [c_int16, c_int32])

""" PICO_STATUS ps4000SetTriggerChannelConditions
    (
        int16_t             handle,
        TRIGGER_CONDITIONS *conditions,
        int16_t             nConditions
    ); """
make_symbol(ldlib, "SetTriggerChannelConditions", "ps4000SetTriggerChannelConditions", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps4000SetTriggerChannelDirections
    (
        int16_t              handle,
        THRESHOLD_DIRECTION  channelA,
        THRESHOLD_DIRECTION  channelB,
        THRESHOLD_DIRECTION  channelC,
        THRESHOLD_DIRECTION  channelD,
        THRESHOLD_DIRECTION  ext,
        THRESHOLD_DIRECTION  aux
    ); """
make_symbol(ldlib, "SetTriggerChannelDirections", "ps4000SetTriggerChannelDirections", c_uint32,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32])

""" PICO_STATUS ps4000SetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
make_symbol(ldlib, "SetTriggerDelay", "ps4000SetTriggerDelay", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps4000SetPulseWidthQualifier
    (
        int16_t              handle,
        PWQ_CONDITIONS      *conditions,
        int16_t              nConditions,
        THRESHOLD_DIRECTION  direction,
        uint32_t             lower,
        uint32_t             upper,
        PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifier", "ps4000SetPulseWidthQualifier", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps4000IsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps4000IsTriggerOrPulseWidthQualifierEnabled", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps4000GetTriggerTimeOffset
    (
        int16_t            handle,
        uint32_t          *timeUpper,
        uint32_t          *timeLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex
    ); """
make_symbol(ldlib, "GetTriggerTimeOffset0", "ps4000GetTriggerTimeOffset", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_uint16])

""" PICO_STATUS ps4000GetTriggerChannelTimeOffset
    (
        int16_t            handle,
        uint32_t          *timeUpper,
        uint32_t          *timeLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex,
        PS4000_CHANNEL     channel
    ); """
make_symbol(ldlib, "GetTriggerChannelTimeOffset0", "ps4000GetTriggerChannelTimeOffset", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_uint16, c_int32])

""" PICO_STATUS ps4000GetTriggerTimeOffset64
    (
        int16_t            handle,
        int64_t           *time,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex
    ); """
make_symbol(ldlib, "GetTriggerTimeOffset", "ps4000GetTriggerTimeOffset64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint16])

""" PICO_STATUS ps4000GetTriggerChannelTimeOffset64
    (
        int16_t            handle,
        int64_t           *time,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex,
        PS4000_CHANNEL     channel
    ); """
make_symbol(ldlib, "GetTriggerChannelTimeOffset64", "ps4000GetTriggerChannelTimeOffset64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint16, c_int32])

""" PICO_STATUS ps4000GetValuesTriggerTimeOffsetBulk
    (
        int16_t            handle,
        uint32_t          *timesUpper,
        uint32_t          *timesLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex
    ); """
make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk0", "ps4000GetValuesTriggerTimeOffsetBulk", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_uint16, c_uint16])

""" PICO_STATUS ps4000GetValuesTriggerChannelTimeOffsetBulk
    (
        int16_t            handle,
        uint32_t          *timesUpper,
        uint32_t          *timesLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex,
        PS4000_CHANNEL     channel
    ); """
make_symbol(ldlib, "GetValuesTriggerChannelTimeOffsetBulk0", "ps4000GetValuesTriggerChannelTimeOffsetBulk", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_uint16, c_uint16, c_int32])

""" PICO_STATUS ps4000GetValuesTriggerTimeOffsetBulk64
    (
        int16_t            handle,
        int64_t           *times,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex
    ); """
make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps4000GetValuesTriggerTimeOffsetBulk64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint16, c_uint16])

""" PICO_STATUS ps4000GetValuesTriggerChannelTimeOffsetBulk64
    (
        int16_t            handle,
        int64_t           *times,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex,
        PS4000_CHANNEL     channel
    ); """
make_symbol(ldlib, "GetValuesTriggerChannelTimeOffsetBulk", "ps4000GetValuesTriggerChannelTimeOffsetBulk64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint16, c_uint16, c_int32])

""" PICO_STATUS ps4000SetDataBufferBulk
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *buffer,
        int32_t         bufferLth,
        uint16_t        waveform
    ); """
make_symbol(ldlib, "SetDataBufferBulk", "ps4000SetDataBufferBulk", c_uint32,
            [c_int16, c_int32, c_void_p, c_int32, c_uint16])

""" PICO_STATUS ps4000SetDataBuffers
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *bufferMax,
        int16_t        *bufferMin,
        int32_t         bufferLth
    ); """
make_symbol(ldlib, "SetDataBuffers", "ps4000SetDataBuffers", c_uint32, [c_int16, c_int32, c_void_p, c_void_p, c_int32])

""" PICO_STATUS ps4000SetDataBufferWithMode
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *buffer,
        int32_t         bufferLth,
        RATIO_MODE      mode
    ); """
make_symbol(ldlib, "SetDataBufferWithMode", "ps4000SetDataBufferWithMode", c_uint32,
            [c_int16, c_int32, c_void_p, c_int32, c_int32])

""" PICO_STATUS ps4000SetDataBuffersWithMode
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *bufferMax,
        int16_t        *bufferMin,
        int32_t         bufferLth,
        RATIO_MODE      mode
    ); """
make_symbol(ldlib, "SetDataBuffersWithMode", "ps4000SetDataBuffersWithMode", c_uint32,
            [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_int32])

""" PICO_STATUS ps4000SetDataBuffer
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *buffer,
        int32_t         bufferLth
    ); """
make_symbol(ldlib, "SetDataBuffer", "ps4000SetDataBuffer", c_uint32, [c_int16, c_int32, c_void_p, c_int32])

""" PICO_STATUS ps4000SetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffer", "ps4000SetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32])

""" PICO_STATUS ps4000SetEtsTimeBuffers
    (
        int16_t   handle,
        uint32_t *timeUpper,
        uint32_t *timeLower,
        int32_t   bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffers", "ps4000SetEtsTimeBuffers", c_uint32, [c_int16, c_void_p, c_void_p, c_int32])

""" PICO_STATUS ps4000RunBlock
    (
        int16_t           handle,
        int32_t           noOfPreTriggerSamples,
        int32_t           noOfPostTriggerSamples,
        uint32_t          timebase,
        int16_t           oversample,
        int32_t          *timeIndisposedMs,
        uint16_t          segmentIndex,
        ps4000BlockReady  lpReady,
        void             *pParameter
    ); """
make_symbol(ldlib, "RunBlock", "ps4000RunBlock", c_uint32,
            [c_int16, c_int32, c_int32, c_uint32, c_int16, c_void_p, c_uint16, c_void_p, c_void_p])

""" PICO_STATUS ps4000RunStreaming
    (
        int16_t            handle,
        uint32_t          *sampleInterval,
        PS4000_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t           maxPreTriggerSamples,
        uint32_t           maxPostPreTriggerSamples,
        int16_t            autoStop,
        uint32_t           downSampleRatio,
        uint32_t           overviewBufferSize
    ); """
make_symbol(ldlib, "RunStreaming", "ps4000RunStreaming", c_uint32,
            [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_uint32])

""" PICO_STATUS ps4000RunStreamingEx
    (
        int16_t            handle,
        uint32_t          *sampleInterval,
        PS4000_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t           maxPreTriggerSamples,
        uint32_t           maxPostPreTriggerSamples,
        int16_t            autoStop,
        uint32_t           downSampleRatio,
        int16_t            downSampleRatioMode,
        uint32_t           overviewBufferSize
    ); """
make_symbol(ldlib, "RunStreamingEx", "ps4000RunStreamingEx", c_uint32,
            [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int16, c_uint32])

""" PICO_STATUS ps4000IsReady
    (
        int16_t handle,
        int16_t * ready
    ); """
make_symbol(ldlib, "IsReady", "ps4000IsReady", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000GetStreamingLatestValues
    (
        int16_t               handle,
        ps4000StreamingReady  lpPs4000Ready,
        void                 *pParameter
    ); """
make_symbol(ldlib, "GetStreamingLatestValues", "ps4000GetStreamingLatestValues", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps4000NoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
make_symbol(ldlib, "NoOfStreamingValues", "ps4000NoOfStreamingValues", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000GetMaxDownSampleRatio
    (
        int16_t   handle,
        uint32_t  noOfUnaggreatedSamples,
        uint32_t *maxDownSampleRatio,
        int16_t   downSampleRatioMode,
        uint16_t  segmentIndex
    ); """
make_symbol(ldlib, "GetMaxDownSampleRatio", "ps4000GetMaxDownSampleRatio", c_uint32,
            [c_int16, c_uint32, c_void_p, c_int16, c_uint16])

""" PICO_STATUS ps4000GetValues
    (
        int16_t   handle,
        uint32_t  startIndex,
        uint32_t *noOfSamples,
        uint32_t  downSampleRatio,
        int16_t   downSampleRatioMode,
        uint16_t  segmentIndex,
        int16_t  *overflow
    ); """
make_symbol(ldlib, "GetValues", "ps4000GetValues", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int16, c_uint16, c_void_p])

""" PICO_STATUS ps4000GetValuesBulk
    (
        int16_t   handle,
        uint32_t *noOfSamples,
        uint16_t  fromSegmentIndex,
        uint16_t  toSegmentIndex,
        int16_t  *overflow
    ); """
make_symbol(ldlib, "GetValuesBulk", "ps4000GetValuesBulk", c_uint32, [c_int16, c_void_p, c_uint16, c_uint16, c_void_p])

""" PICO_STATUS ps4000GetValuesAsync
    (
        int16_t   handle,
        uint32_t  startIndex,
        uint32_t  noOfSamples,
        uint32_t  downSampleRatio,
        int16_t   downSampleRatioMode,
        uint16_t  segmentIndex,
        void     *lpDataReady,
        void     *pParameter
    ); """
make_symbol(ldlib, "GetValuesAsync", "ps4000GetValuesAsync", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_int16, c_uint16, c_void_p, c_void_p])

""" PICO_STATUS ps4000Stop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps4000Stop", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000SetProbe
    (
        int16_t       handle,
        PS4000_PROBE  probe,
        PS4000_RANGE  range
    ); """
make_symbol(ldlib, "SetProbe", "ps4000SetProbe", c_uint32, [c_int16, c_int32, c_int32])

""" PICO_STATUS ps4000HoldOff
    (
        int16_t              handle,
        uint64_t             holdoff,
        PS4000_HOLDOFF_TYPE  type
    ); """
make_symbol(ldlib, "HoldOff", "ps4000HoldOff", c_uint32, [c_int16, c_uint64, c_int32])

""" PICO_STATUS ps4000GetProbe
    (
        int16_t       handle,
        PS4000_PROBE *probe
    ); """
make_symbol(ldlib, "GetProbe", "ps4000GetProbe", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000GetChannelInformation
    (
        int16_t              handle,
        PS4000_CHANNEL_INFO  info,
        int32_t              probe,
        int32_t             *ranges,
        int32_t             *length,
        int32_t              channels
    ); """
make_symbol(ldlib, "GetChannelInformation", "ps4000GetChannelInformation", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32])

""" PICO_STATUS ps4000SetFrequencyCounter
    (
        int16_t                         handle,
        PS4000_CHANNEL                  channel,
        int16_t                         enabled,
        PS4000_FREQUENCY_COUNTER_RANGE  range,
        int16_t                         thresholdMajor,
        int16_t                         thresholdMinor
    ); """
make_symbol(ldlib, "SetFrequencyCounter", "ps4000SetFrequencyCounter", c_uint32,
            [c_int16, c_int32, c_int16, c_int32, c_int16, c_int16])

""" PICO_STATUS ps4000EnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
make_symbol(ldlib, "EnumerateUnits", "ps4000EnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p])

""" PICO_STATUS ps4000PingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps4000PingUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000SetBwFilter
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t         enable
    ); """
make_symbol(ldlib, "SetBwFilter", "ps4000SetBwFilter", c_uint32, [c_int16, c_int32, c_int16])

""" PICO_STATUS ps4000TriggerWithinPreTriggerSamples
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "TriggerWithinPreTriggerSamples", "ps4000TriggerWithinPreTriggerSamples", c_uint32,
            [c_int16, c_int16])

""" PICO_STATUS ps4000GetNoOfCaptures
    (
        int16_t   handle,
        uint16_t *nCaptures
    ); """
make_symbol(ldlib, "GetNoOfCaptures", "ps4000GetNoOfCaptures", c_uint32, [c_int16, c_void_p])


class RatioModes(dict2class):
    """ Collection of Downsample modes """
    raw = 0
    none = raw
    agg = 1
    aggregate = agg
    avg = 2
    average = avg
    map = (raw, agg, avg)
    labels = {raw: "raw", agg: "agg", avg: "avg"}

    @staticmethod
    def mode2dict(mode):
        """ returns dict of matched modes """
        r = {}
        for m in RatioModes.labels:
            if mode == m:
                return {RatioModes.labels[m]: m}
            if mode & m > 0:
                r[RatioModes.labels[m]] = m
        return r

    @staticmethod
    def isvalid(mode):
        return len(RatioModes.mode2dict(mode)) > 0

    @staticmethod
    def issingle(mode):
        return mode in RatioModes.labels.keys()

variants = ("4424", "4423", "4223", "4224", "4226", "4226", "4227", "4262")


class Device(ps5000base.PS5000Device):
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
        self.info.min_range = self.m.Ranges.r50mv
        self.info.max_range = self.m.Ranges.r20v
        if self.info.variant_info == "4424":
            self.info.num_channels = 4
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r100v
        elif self.info.variant_info == "4423":
            self.info.num_channels = 2
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r100v
        elif self.info.variant_info == "4223":
            self.info.num_channels = 2
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r100v
        elif self.info.variant_info == "4224":
            self.info.num_channels = 2
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r100v
        elif self.info.variant_info == "4226":
            self.info.num_channels = 2
            self.info.has_siggen = True
            self.info.siggen_frequency = 100000
            self.info.siggen_min = 500000
            self.info.siggen_max = 2000000
            self.info.has_awg = True
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r100v
        elif self.info.variant_info == "4226":
            self.info.num_channels = 2
            self.info.has_siggen = True
            self.info.siggen_frequency = 100000
            self.info.siggen_min = 500000
            self.info.siggen_max = 2000000
            self.info.has_awg = True
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r100v
        elif self.info.variant_info == "4227":
            self.info.num_channels = 2
            self.info.has_siggen = True
            self.info.siggen_frequency = 100000
            self.info.siggen_min = 500000
            self.info.siggen_max = 2000000
            self.info.has_awg = True
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r100v
        elif self.info.variant_info == "4262":
            self.info.num_channels = 2
            self.info.has_siggen = True
            self.info.siggen_frequency = 100000
            self.info.siggen_min = 500000
            self.info.siggen_max = 2000000
            self.info.has_awg = False
            self.info.max_segments = 32768
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
        else:
            return pico_num("PICO_INFO_UNAVAILABLE")
        return pico_num("PICO_OK")

    def _set_memory_info(self):
        """
        Sets initial memory setup
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        self._buffers = {}
        self._segments = 1
        mem = c_int32()
        status = self._memory_segments(self._segments, byref(mem))
        self.info.memory = mem.value
        self.info.memps = mem.value
        return status

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
        status = ldlib.SetChannel(self._chandle, c_int32(channel), c_int16(state.enabled),
                                  c_int16(1 if state.coupling == self.m.Couplings.dc else 0), c_int32(state.range))
        if status == pico_num("PICO_OK"):
            state.overvoltaged = False
            self._channel_set[channel] = deepcopy(state)
        return status

    def collect_segment_overlapped(self, segment, interval=None, event_handle=None, timebase=None, block=True):
        return pico_num("PICO_NOT_SUPPORTED_BY_THIS_DEVICE")

    def _memory_segments(self, segments, ref_mem):
        return ldlib.MemorySegments(self._chandle, c_uint16(segments), ref_mem)

    def _set_sig_gen_built_in(self, offset, pk2pk, wave, start, stop, increment, dwelltime,
                              sweep, extra, shots, sweeps, trigt, trigs, threshold):

        return ldlib.SetSigGenBuiltIn(self._chandle, c_int32(offset), c_uint32(pk2pk), c_int16(wave),
                                      c_float(start), c_float(stop), c_float(increment), c_float(dwelltime),
                                      c_int32(sweep), c_int16(extra), c_uint32(shots), c_uint32(sweeps),
                                      c_int32(trigt), c_int32(trigs), c_int16(threshold))

    def _set_sig_gen_arbitrary(self, offset, pk2pk, phase_start, phase_stop, phase_inc, dwell, ref_wave, bufflen,
                               sweep, extra, mode, shots, sweeps, trigt, trigs, threshold):
        return ldlib.SetSigGenArbitrary(self._chandle, c_int32(offset), c_uint32(pk2pk), c_uint32(phase_start),
                                        c_uint32(phase_stop), c_uint32(phase_inc), c_uint32(dwell), ref_wave,
                                        c_int32(bufflen), c_int32(sweep), c_int16(extra), c_int32(mode),
                                        c_uint32(shots), c_uint32(sweeps), c_int32(trigt), c_int32(trigs),
                                        c_int16(threshold))

    def _get_timebase(self, timebase, samples, ref_interval, oversample, ref_maxsamples, segment):
        return ldlib.GetTimebase(self._chandle, c_uint32(timebase), c_int32(samples), ref_interval, c_int16(oversample),
                                 ref_maxsamples, c_uint16(segment))

    def _run_block(self, pretrig, posttrig, timebase, oversample, ref_time, segment, ref_cb, ref_cb_param):
        return ldlib.RunBlock(self._chandle, c_int32(pretrig), c_int32(posttrig), c_uint32(timebase),
                              c_int16(oversample), ref_time, c_uint16(segment), ref_cb, ref_cb_param)

    def _run_streaming(self, ref_interval, units, pretrig, posttrig, autostop, ratio, mode, overview):
        return ldlib.RunStreaming(self._chandle, ref_interval, c_int32(units), c_uint32(pretrig), c_uint32(posttrig),
                                  c_int16(autostop), c_uint32(ratio), c_uint32(overview))

    def _get_values(self, start, ref_samples, ratio, mode, segment, ref_overflow):
        return ldlib.GetValues(self._chandle, c_uint32(start), ref_samples,
                               c_uint32(ratio), c_int16(mode), c_uint16(segment), ref_overflow)

    def _get_values_bulk(self, ref_samples, start_segment, stop_segment, ratio, mode, ref_overflow):
        return ldlib.GetValuesBulk(self._chandle, ref_samples,
                                   c_uint16(start_segment), c_uint16(stop_segment), ref_overflow)

    def _get_values_async(self, start, samples, ratio, mode, segment, ref_cb, ref_cb_param):
        return ldlib.GetValuesAsync(self._chandle, c_uint32(start), c_uint32(samples), c_uint32(ratio), c_int16(mode),
                                    c_uint16(segment), ref_cb, ref_cb_param)

    def _get_trigger_time_offset(self, ref_offsets, ref_units, segment):
        return ldlib.GetTriggerTimeOffset(self._chandle, ref_offsets, ref_units, c_uint16(segment))

    def _get_values_trigger_time_offset_bulk(self, ref_offsets, ref_units, start_segment, stop_segment):
        return ldlib.GetValuesTriggerTimeOffsetBulk(self._chandle, ref_offsets, ref_units,
                                                    c_uint16(start_segment), c_uint16(stop_segment))

    def _set_data_buffers(self, line, buffer_max, buffer_min, bufflen, segment, mode):
        return ldlib.SetDataBuffersWithMode(self._chandle, c_int32(line), buffer_max, buffer_min,
                                            c_int32(bufflen), c_int32(mode))

    def _set_no_of_captures(self, number):
        return ldlib.SetNoOfCaptures(self._chandle, c_uint16(number))

    @staticmethod
    def _data_ready():
        if sys.platform == 'win32':
            return WINFUNCTYPE(None, c_int16, c_int32, c_int16, c_uint32, c_int16, c_void_p)
        else:
            return CFUNCTYPE(None, c_int16, c_int32, c_int16, c_uint32, c_int16, c_void_p)


def enumerate_units():
    global ldlib
    return ps5000base.enumerate_units(ldlib)
