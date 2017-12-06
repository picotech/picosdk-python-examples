#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps5000aApi.h C header
file for PicoScope 5000 Series oscilloscopes using the ps5000a driver API
functions.
"""

from ps5000base import *
from psutils import *
from picosdk import ps5000base

name = "ps5000a"
_libps5000a = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps5000a
ldlib.name = name

""" PICO_STATUS (ps5000aOpenUnit)
    (
        int16_t                   *handle,
        int8_t                    *serial,
        PS5000A_DEVICE_RESOLUTION  resolution
    ); """
make_symbol(ldlib, "OpenUnit", "ps5000aOpenUnit", c_uint32, [c_void_p, c_char_p, c_int32])

""" PICO_STATUS ps5000aOpenUnitAsync
    (
        int16_t                   *status,
        int8_t                    *serial,
        PS5000A_DEVICE_RESOLUTION  resolution
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps5000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p, c_int32])

""" PICO_STATUS ps5000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps5000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps5000aGetUnitInfo
    (
        int16_t   handle,
        int8_t   *string,
        int16_t   stringLength,
        int16_t  *requiredSize,
        PICO_INFO info
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps5000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps5000aFlashLed
    (
        int16_t handle,
        int16_t start
    ); """
make_symbol(ldlib, "FlashLed", "ps5000aFlashLed", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps5000aIsLedFlashing
    (
        int16_t  handle,
        int16_t *status
    ); """
make_symbol(ldlib, "IsLedFlashing", "ps5000aIsLedFlashing", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aCloseUnit
    (
        int16_t handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps5000aCloseUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps5000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
make_symbol(ldlib, "MemorySegments", "ps5000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p])

""" PICO_STATUS ps5000aSetChannel
    (
        int16_t          handle,
        PS5000a_CHANNEL  channel,
        int16_t          enabled,
        PS5000a_COUPLING type,
        PS5000a_RANGE    range,
        float            analogOffset
    ); """
make_symbol(ldlib, "SetChannel", "ps5000aSetChannel", c_uint32, [c_int16, c_int32, c_int16, c_int32, c_int32, c_float])

""" PICO_STATUS ps5000aSetBandwidthFilter
    (
        int16_t                    handle,
        PS5000A_CHANNEL            channel,
        PS5000A_BANDWIDTH_LIMITER  bandwidth
    ); """
make_symbol(ldlib, "SetBandwidthFilter", "ps5000aSetBandwidthFilter", c_uint32, [c_int16, c_int32, c_int32])

""" PICO_STATUS ps5000aGetTimebase2
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        float    *timeIntervalNanoseconds,
        int32_t  *maxSamples,
        uint32_t  segmentIndex
    ); """
make_symbol(ldlib, "GetTimebase", "ps5000aGetTimebase2", c_uint32,
            [c_int16, c_uint32, c_int32, c_void_p, c_void_p, c_uint32])

""" PICO_STATUS ps5000aSetSigGenArbitrary
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        int16_t                    *arbitraryWaveform,
        int32_t                     arbitraryWaveformSize,
        PS5000A_SWEEP_TYPE          sweepType,
        PS5000A_EXTRA_OPERATIONS    operation,
        PS5000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenArbitrary", "ps5000aSetSigGenArbitrary", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32, c_int32,
             c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps5000aSetSigGenBuiltInV2
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        PS5000A_WAVE_TYPE           waveType,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS5000A_SWEEP_TYPE          sweepType,
        PS5000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenBuiltIn", "ps5000aSetSigGenBuiltInV2", c_uint32,
            [c_int16, c_int32, c_uint32, c_int32, c_double, c_double, c_double, c_double,
             c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps5000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS5000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesArbitrary", "ps5000aSetSigGenPropertiesArbitrary", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps5000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS5000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesBuiltIn", "ps5000aSetSigGenPropertiesBuiltIn", c_uint32,
            [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps5000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS5000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
make_symbol(ldlib, "SigGenFrequencyToPhase", "ps5000aSigGenFrequencyToPhase", c_uint32,
            [c_int16, c_double, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps5000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
make_symbol(ldlib, "SigGenArbitraryMinMaxValues", "ps5000aSigGenArbitraryMinMaxValues", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps5000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "SigGenSoftwareControl", "ps5000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps5000aSetEts
    (
        int16_t           handle,
        PS5000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
make_symbol(ldlib, "SetEts", "ps5000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

""" PICO_STATUS ps5000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS5000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetTriggerChannelProperties", "ps5000aSetTriggerChannelProperties", c_uint32,
            [c_int16, c_void_p, c_int16, c_int16, c_int32])

""" PICO_STATUS ps5000aSetTriggerChannelConditions
    (
        int16_t                     handle,
        PS5000A_TRIGGER_CONDITIONS *conditions,
        int16_t                     nConditions
    ); """
make_symbol(ldlib, "SetTriggerChannelConditions", "ps5000aSetTriggerChannelConditions", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps5000aSetTriggerChannelDirections
    (
        int16_t                      handle,
        PS5000A_THRESHOLD_DIRECTION  channelA,
        PS5000A_THRESHOLD_DIRECTION  channelB,
        PS5000A_THRESHOLD_DIRECTION  channelC,
        PS5000A_THRESHOLD_DIRECTION  channelD,
        PS5000A_THRESHOLD_DIRECTION  ext,
        PS5000A_THRESHOLD_DIRECTION  aux
    ); """
make_symbol(ldlib, "SetTriggerChannelDirections", "ps5000aSetTriggerChannelDirections", c_uint32,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32])

""" PICO_STATUS ps5000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS5000A_CHANNEL              source,
        int16_t                      threshold,
        PS5000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
make_symbol(ldlib, "SetSimpleTrigger", "ps5000aSetSimpleTrigger", c_uint32,
            [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

""" PICO_STATUS ps5000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
make_symbol(ldlib, "SetTriggerDelay", "ps5000aSetTriggerDelay", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps5000aSetPulseWidthQualifier
    (
        int16_t                      handle,
        PS5000A_PWQ_CONDITIONS      *conditions,
        int16_t                      nConditions,
        PS5000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS5000A_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifier", "ps5000aSetPulseWidthQualifier", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps5000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps5000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps5000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS5000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
make_symbol(ldlib, "GetTriggerTimeOffset", "ps5000aGetTriggerTimeOffset64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32])

""" PICO_STATUS ps5000aGetValuesTriggerTimeOffsetBulk64
    (
        int16_t             handle,
        int64_t            *times,
        PS5000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps5000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32, c_uint32])

""" PICO_STATUS ps5000aSetDataBuffers
    (
        int16_t            handle,
        PS5000A_CHANNEL    channel,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS5000A_RATIO_MODE mode
    ); """
make_symbol(ldlib, "SetDataBuffers", "ps5000aSetDataBuffers",
            c_uint32, [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps5000aSetDataBuffer
    (
        int16_t            handle,
        PS5000A_CHANNEL    channel,
        int16_t           *buffer,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS5000A_RATIO_MODE mode
    ); """
make_symbol(ldlib, "SetDataBuffer", "ps5000aSetDataBuffer",
            c_uint32, [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps5000aSetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffer", "ps5000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32])

""" PICO_STATUS ps5000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
make_symbol(ldlib, "IsReady", "ps5000aIsReady", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps5000aBlockReady  lpReady,
        void              *pParameter
    ); """
make_symbol(ldlib, "RunBlock", "ps5000aRunBlock", c_uint32,
            [c_int16, c_int32, c_int32, c_uint32, c_void_p, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps5000aRunStreaming
    (
        int16_t             handle,
        uint32_t            *sampleInterval,
        PS5000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostPreTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
make_symbol(ldlib, "RunStreaming", "ps5000aRunStreaming", c_uint32,
            [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32])

""" PICO_STATUS ps5000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps5000aStreamingReady  lpPs5000aReady,
        void                  *pParameter
    ); """
make_symbol(ldlib, "GetStreamingLatestValues", "ps5000aGetStreamingLatestValues", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" void *ps5000aStreamingReady
    (
        int16_t   handle,
        int32_t   noOfSamples,
        uint32_t  startIndex,
        int16_t   overflow,
        uint32_t  triggerAt,
        int16_t   triggered,
        int16_t   autoStop,
        void     *pParameter
    ); """

""" PICO_STATUS ps5000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
make_symbol(ldlib, "NoOfStreamingValues", "ps5000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aGetMaxDownSampleRatio
    (
        int16_t             handle,
        uint32_t            noOfUnaggreatedSamples,
        uint32_t           *maxDownSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex
    ); """
make_symbol(ldlib, "GetMaxDownSampleRatio", "ps5000aGetMaxDownSampleRatio", c_uint32,
            [c_int16, c_uint32, c_void_p, c_int32, c_uint32])

""" PICO_STATUS ps5000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS5000a_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValues", "ps5000aGetValues", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps5000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
make_symbol(ldlib, "GetValuesAsync", "ps5000aGetValuesAsync", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps5000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesBulk", "ps5000aGetValuesBulk", c_uint32,
            [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p])

""" PICO_STATUS ps5000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlapped", "ps5000aGetValuesOverlapped", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps5000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlappedBulk", "ps5000aGetValuesOverlappedBulk", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p])

""" PICO_STATUS ps5000aTriggerWithinPreTriggerSamples
    (
        int16_t                             handle,
        PS5000A_TRIGGER_WITHIN_PRE_TRIGGER  state
    ); """
make_symbol(ldlib, "TriggerWithinPreTriggerSamples", "ps5000aTriggerWithinPreTriggerSamples", c_uint32,
            [c_int16, c_int32])

""" PICO_STATUS ps5000aGetTriggerInfoBulk
    (
        int16_t               handle,
        PS5000A_TRIGGER_INFO *triggerInfo,
        uint32_t              fromSegmentIndex,
        uint32_t              toSegmentIndex
    ); """
make_symbol(ldlib, "GetTriggerInfoBulk", "ps5000aGetTriggerInfoBulk", c_uint32, [c_int16, c_void_p, c_uint32, c_uint32])

""" PICO_STATUS ps5000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
make_symbol(ldlib, "EnumerateUnits", "ps5000aEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p])

""" PICO_STATUS ps5000aGetChannelInformation
    (
        int16_t               handle,
        PS5000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
make_symbol(ldlib, "GetChannelInformation", "ps5000aGetChannelInformation", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32])

""" PICO_STATUS ps5000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
make_symbol(ldlib, "MaximumValue", "ps5000aMaximumValue", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aMinimumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
make_symbol(ldlib, "MinimumValue", "ps5000aMinimumValue", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aGetAnalogueOffset
    (
        int16_t           handle,
        PS5000A_RANGE     range,
        PS5000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
make_symbol(ldlib, "GetAnalogueOffset", "ps5000aGetAnalogueOffset", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p])

""" PICO_STATUS ps5000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
make_symbol(ldlib, "GetMaxSegments", "ps5000aGetMaxSegments", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aChangePowerSource
    (
        int16_t     handle,
        PICO_STATUS powerState
    ); """
make_symbol(ldlib, "ChangePowerSource", "ps5000aChangePowerSource", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps5000aCurrentPowerSource
    (
        int16_t handle
    ); """
make_symbol(ldlib, "CurrentPowerSource", "ps5000aCurrentPowerSource", c_uint32, [c_int16, ])

""" PICO_STATUS ps5000aStop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps5000aStop", c_uint32, [c_int16, ])

""" PICO_STATUS ps5000aPingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps5000aPingUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps5000aSetNoOfCaptures
    (
        int16_t   handle,
        uint32_t  nCaptures
    ); """
make_symbol(ldlib, "SetNoOfCaptures", "ps5000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps5000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
make_symbol(ldlib, "GetNoOfCaptures", "ps5000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aGetNoOfProcessedCaptures
    (
          int16_t   handle,
          uint32_t *nProcessedCaptures
    ); """
make_symbol(ldlib, "GetNoOfProcessedCaptures", "ps5000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps5000aSetDeviceResolution
    (
      int16_t                    handle,
      PS5000A_DEVICE_RESOLUTION  resolution
    ); """
make_symbol(ldlib, "SetDeviceResolution", "ps5000aSetDeviceResolution", c_uint32, [c_int16, c_int32])

""" PICO_STATUS ps5000aGetDeviceResolution
    (
        int16_t                    handle,
        PS5000A_DEVICE_RESOLUTION *resolution
    ); """
make_symbol(ldlib, "GetDeviceResolution", "ps5000aGetDeviceResolution", c_uint32, [c_int16, c_void_p])


class Resolutions(dict2class):
    res8bit = 0
    res12bit = 1
    res14bit = 2
    res15bit = 3
    res16bit = 4
    labels = {res8bit: "8 bit", res12bit: "12 bit", res14bit: "14 bit", res15bit: "15 bit", res16bit: "16 bit"}

variants = ("5242A", "5242B", "5243A", "5243B", "5244A", "5244B", "5442A", "5442B", "5443A", "5443B", "5444A", "5444B")


class Device(PS5000Device):
    def __init__(self):
        self.m = sys.modules[__name__]
        super(Device, self).__init__(ldlib)
        self.info.resolution = Resolutions.res8bit

    def open_unit(self, serial=None, resolution=Resolutions.res8bit):
        """ Opens unit
        :param serial: string specifying device serial and batch
        :type serial: string
        :param resolution: optional resolution enum
        :type resolution: int
        :returns: status of the call
        :rtype: int
        """
        """ Only one unit allowed per instance """
        if self._handle > 0:
            """ same will occur if 64 devices are opened... unlikely"""
            return pico_num("PICO_MAX_UNITS_OPENED")
        try:
            status = ldlib.OpenUnit(byref(self._chandle), c_char_p(serial), c_int32(resolution))
        except AttributeError:
            print "Library not loaded"
            return pico_num("PICO_NOT_FOUND")

        self._handle = self._chandle.value
        self.info.handle = self._handle
        """ Read INFO from device, populate self.info """
        if status == pico_num("PICO_OK"):
            status = self.load_info()
        return status

    def load_info(self):
        """
        Allows to continue loading after initial failure
        """
        status = self._set_info()
        if status == pico_num("PICO_OK"):
            """ Set device defaults """
            status = self.set_defaults()
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
        self.info.num_ports = 0
        self.info.min_range = Ranges.r10mv
        self.info.max_range = Ranges.r20v
        self.info.has_siggen = True
        self.info.siggen_frequency = 1000000
        self.info.siggen_min = 0
        self.info.siggen_max = 4000000
        self.info.has_ets = True
        if self.info.variant_info == "5242A":
            self.info.num_channels = 2
            self.info.has_awg = False
        elif self.info.variant_info == "5242B":
            self.info.num_channels = 2
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "5243A":
            self.info.num_channels = 2
            self.info.has_awg = False
        elif self.info.variant_info == "5243B":
            self.info.num_channels = 2
            self.info.has_awg = True
            self.info.awg_size = 32768
        elif self.info.variant_info == "5244A":
            self.info.num_channels = 2
            self.info.has_awg = False
        elif self.info.variant_info == "5244B":
            self.info.num_channels = 2
            self.info.has_awg = True
            self.info.awg_size = 49152
        elif self.info.variant_info == "5442A":
            self.info.num_channels = 4
            self.info.has_awg = False
        elif self.info.variant_info == "5442B":
            self.info.num_channels = 4
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "5443A":
            self.info.num_channels = 4
            self.info.has_awg = False
        elif self.info.variant_info == "5443B":
            self.info.num_channels = 4
            self.info.has_awg = True
            self.info.awg_size = 32768
        elif self.info.variant_info == "5444A":
            self.info.num_channels = 4
            self.info.has_awg = False
        elif self.info.variant_info == "5444B":
            self.info.num_channels = 4
            self.info.has_awg = True
            self.info.awg_size = 49152
        else:
            return pico_num("PICO_INFO_UNAVAILABLE")
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
            state = ChannelState()
            state.enabled = False
            state.coupling = Couplings.dc
            state.range = Ranges.r500mv
            state.offset = 0
            self.set_channel(Channels.map[channel], state)
        return pico_num("PICO_OK")

    def set_power_source(self, power):
        """ Resets/acknowledges power source setting for the device
        :param power: power status to acknowledge/reset
        :type power: int
        :return: further power status
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        if power == pico_num("PICO_OK"):
            return power
        return ldlib.ChangePowerSource(self._chandle, c_uint32(power))

    def set_device_resolution(self, resolution):
        """ Set device ADC resolution
        :param resolution: enum as in Resolutions
        :type resolution: int
        :return: status of the call
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")
        status = ldlib.SetDeviceResolution(self._chandle, c_int32(resolution))
        if status == pico_num("PICO_OK"):
            self.info.resolution = resolution
        return status

    def _set_sig_gen_built_in(self, offset, pk2pk, wave, start, stop, increment, dwelltime,
                              sweep, extra, shots, sweeps, trigt, trigs, threshold):

        return ldlib.SetSigGenBuiltIn(self._chandle, c_int32(offset), c_uint32(pk2pk), c_int32(wave),
                                      c_double(start), c_double(stop), c_double(increment), c_double(dwelltime),
                                      c_int32(sweep), c_int32(extra), c_uint32(shots), c_uint32(sweeps),
                                      c_int32(trigt), c_int32(trigs), c_int16(threshold))

    def _get_timebase(self, timebase, samples, ref_interval, oversample, ref_maxsamples, segment):
        return ldlib.GetTimebase(self._chandle, c_uint32(timebase), c_int32(samples), ref_interval,
                                 ref_maxsamples, c_uint32(segment))

    def _run_block(self, pretrig, posttrig, timebase, oversample, ref_time, segment, ref_cb, ref_cb_param):
        return ldlib.RunBlock(self._chandle, c_int32(pretrig), c_int32(posttrig), c_uint32(timebase),
                              ref_time, c_uint32(segment), ref_cb, ref_cb_param)


def enumerate_units():
    global ldlib
    return ps5000base.enumerate_units(ldlib)
