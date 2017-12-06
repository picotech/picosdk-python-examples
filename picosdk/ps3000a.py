#
# Copyright (C) 2014-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps3000aApi.h C header
file for PicoScope 3000 Series oscilloscopes using the ps3000a driver API
functions.
"""

from ps5000base import *
from psutils import *
from picosdk import ps5000base

name = "ps3000a"
_libps3000a = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps3000a
ldlib.name = name

""" PICO_STATUS ps3000aOpenUnit
    (
        int16_t *handle,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnit", "ps3000aOpenUnit", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps3000aOpenUnitAsync
    (
        int16_t *status,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps3000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps3000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps3000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps3000aGetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t   *requiredSize,
        PICO_INFO  info
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps3000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps3000aFlashLed
    (
        int16_t  handle,
        int16_t  start
    ); """
make_symbol(ldlib, "FlashLed", "ps3000aFlashLed", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps3000aCloseUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps3000aCloseUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps3000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
make_symbol(ldlib, "MemorySegments", "ps3000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p])

""" PICO_STATUS ps3000aSetChannel
    (
        int16_t          handle,
        PS3000a_CHANNEL  channel,
        int16_t          enabled,
        PS3000a_COUPLING type,
        PS3000a_RANGE    range,
        float            analogOffset
    ); """
make_symbol(ldlib, "SetChannel", "ps3000aSetChannel", c_uint32, [c_int16, c_int32, c_int16, c_int32, c_int32, c_float])

""" PICO_STATUS ps3000aSetDigitalPort
    (
        int16_t              handle,
        PS3000a_DIGITAL_PORT port,
        int16_t              enabled,
        int16_t              logicLevel
    ); """
make_symbol(ldlib, "SetDigitalPort", "ps3000aSetDigitalPort", c_uint32, [c_int16, c_int32, c_int16, c_int16])

""" PICO_STATUS ps3000aSetBandwidthFilter
    (
        int16_t                    handle,
        PS3000A_CHANNEL            channel,
        PS3000A_BANDWIDTH_LIMITER  bandwidth
    ); """
make_symbol(ldlib, "SetBandwidthFilter", "ps3000aSetBandwidthFilter", c_uint32, [c_int16, c_int32, c_int32])

""" PICO_STATUS ps3000aSetNoOfCaptures
    (
        int16_t   handle,
        uint32_t  nCaptures
    ); """
make_symbol(ldlib, "SetNoOfCaptures", "ps3000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps3000aGetTimebase2
    (
        int16_t  handle,
        uint32_t timebase,
        int32_t  noSamples,
        float   *timeIntervalNanoseconds,
        int16_t  oversample,
        int32_t *maxSamples,
        uint32_t segmentIndex
    ); """
make_symbol(ldlib, "GetTimebase", "ps3000aGetTimebase2", c_uint32,
            [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps3000aSetSigGenArbitrary
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
        PS3000A_SWEEP_TYPE          sweepType,
        PS3000A_EXTRA_OPERATIONS    operation,
        PS3000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenArbitrary", "ps3000aSetSigGenArbitrary", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32, c_int32,
             c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps3000aSetSigGenBuiltIn
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        int16_t                     waveType,
        float                       startFrequency,
        float                       stopFrequency,
        float                       increment,
        float                       dwellTime,
        PS3000A_SWEEP_TYPE          sweepType,
        PS3000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenBuiltIn", "ps3000aSetSigGenBuiltIn", c_uint32,
            [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float, c_int32, c_int32, c_uint32,
             c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps3000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS3000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesArbitrary", "ps3000aSetSigGenPropertiesArbitrary", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps3000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS3000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesBuiltIn", "ps3000aSetSigGenPropertiesBuiltIn", c_uint32,
            [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps3000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS3000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
make_symbol(ldlib, "SigGenFrequencyToPhase", "ps3000aSigGenFrequencyToPhase", c_uint32,
            [c_int16, c_double, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps3000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
make_symbol(ldlib, "SigGenArbitraryMinMaxValues", "ps3000aSigGenArbitraryMinMaxValues", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps3000aGetMaxEtsValues
    (
        int16_t  handle,
        int16_t *etsCycles,
        int16_t *etsInterleave
    ); """
make_symbol(ldlib, "GetMaxEtsValues", "ps3000aGetMaxEtsValues", c_uint32, [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps3000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "SigGenSoftwareControl", "ps3000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps3000aSetEts
    (
        int16_t           handle,
        PS3000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
make_symbol(ldlib, "SetEts", "ps3000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

""" PICO_STATUS ps3000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS3000A_CHANNEL              source,
        int16_t                      threshold,
        PS3000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
make_symbol(ldlib, "SetSimpleTrigger", "ps3000aSetSimpleTrigger", c_uint32,
            [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

""" PICO_STATUS ps3000aSetTriggerDigitalPortProperties
    (
        int16_t                             handle,
        PS3000A_DIGITAL_CHANNEL_DIRECTIONS *directions,
        int16_t                             nDirections
    ); """
make_symbol(ldlib, "SetTriggerDigitalPortProperties", "ps3000aSetTriggerDigitalPortProperties", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps3000aSetPulseWidthDigitalPortProperties
    (
        int16_t                             handle,
        PS3000A_DIGITAL_CHANNEL_DIRECTIONS *directions,
        int16_t                             nDirections
    ); """
make_symbol(ldlib, "SetPulseWidthDigitalPortProperties", "ps3000aSetPulseWidthDigitalPortProperties", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps3000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS3000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetTriggerChannelProperties", "ps3000aSetTriggerChannelProperties", c_uint32,
            [c_int16, c_void_p, c_int16, c_int16, c_int32])

""" PICO_STATUS ps3000aSetTriggerChannelConditions
    (
        int16_t                     handle,
        PS3000A_TRIGGER_CONDITIONS *conditions,
        int16_t                     nConditions
    ); """
make_symbol(ldlib, "SetTriggerChannelConditions", "ps3000aSetTriggerChannelConditions", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps3000aSetTriggerChannelConditionsV2
    (
        int16_t                        handle,
        PS3000A_TRIGGER_CONDITIONS_V2 *conditions,
        int16_t                        nConditions
    ); """
make_symbol(ldlib, "SetTriggerChannelConditionsV2", "ps3000aSetTriggerChannelConditionsV2", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps3000aSetTriggerChannelDirections
    (
        int16_t                      handle,
        PS3000A_THRESHOLD_DIRECTION  channelA,
        PS3000A_THRESHOLD_DIRECTION  channelB,
        PS3000A_THRESHOLD_DIRECTION  channelC,
        PS3000A_THRESHOLD_DIRECTION  channelD,
        PS3000A_THRESHOLD_DIRECTION  ext,
        PS3000A_THRESHOLD_DIRECTION  aux
    ); """
make_symbol(ldlib, "SetTriggerChannelDirections", "ps3000aSetTriggerChannelDirections", c_uint32,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32])

""" PICO_STATUS ps3000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
make_symbol(ldlib, "SetTriggerDelay", "ps3000aSetTriggerDelay", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps3000aSetPulseWidthQualifier
    (
        int16_t                      handle,
        PS3000A_PWQ_CONDITIONS      *conditions,
        int16_t                      nConditions,
        PS3000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS3000A_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifier", "ps3000aSetPulseWidthQualifier", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps3000aSetPulseWidthQualifierV2
    (
        int16_t                      handle,
        PS3000A_PWQ_CONDITIONS_V2   *conditions,
        int16_t                      nConditions,
        PS3000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS3000A_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifierV2", "ps3000aSetPulseWidthQualifierV2", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps3000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps3000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps3000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS3000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
make_symbol(ldlib, "GetTriggerTimeOffset", "ps3000aGetTriggerTimeOffset64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32])

""" PICO_STATUS ps3000aGetValuesTriggerTimeOffsetBulk64
    (
        int16_t             handle,
        int64_t            *times,
        PS3000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps3000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32, c_uint32])

""" PICO_STATUS ps3000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
make_symbol(ldlib, "GetNoOfCaptures", "ps3000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps3000aGetNoOfProcessedCaptures
    (
        int16_t   handle,
        uint32_t *nProcessedCaptures
    ); """
make_symbol(ldlib, "GetNoOfProcessedCaptures", "ps3000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps3000aSetDataBuffer
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *buffer,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS3000a_RATIO_MODE mode
    ); """
make_symbol(ldlib, "SetDataBuffer", "ps3000aSetDataBuffer", c_uint32,
            [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps3000aSetDataBuffers
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS3000a_RATIO_MODE mode
    ); """
make_symbol(ldlib, "SetDataBuffers", "ps3000aSetDataBuffers", c_uint32,
            [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps3000aSetEtsTimeBuffer
    (
        int16_t    handle,
        int64_t *buffer,
        int32_t     bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffer", "ps3000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32])

""" PICO_STATUS ps3000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
make_symbol(ldlib, "IsReady", "ps3000aIsReady", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps3000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int16_t            oversample,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps3000aBlockReady  lpReady,
        void              *pParameter
    ); """
make_symbol(ldlib, "RunBlock", "ps3000aRunBlock", c_uint32,
            [c_int16, c_int32, c_int32, c_uint32, c_int16, c_void_p, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps3000aRunStreaming
    (
        int16_t             handle,
        uint32_t            *sampleInterval,
        PS3000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostPreTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
make_symbol(ldlib, "RunStreaming", "ps3000aRunStreaming", c_uint32,
            [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32])

""" PICO_STATUS ps3000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps3000aStreamingReady  lpPs3000aReady,
        void                   *pParameter
    ); """
make_symbol(ldlib, "GetStreamingLatestValues", "ps3000aGetStreamingLatestValues", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" void *ps3000aStreamingReady
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

""" PICO_STATUS ps3000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
make_symbol(ldlib, "NoOfStreamingValues", "ps3000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps3000aGetMaxDownSampleRatio
(
  int16_t               handle,
  uint32_t       noOfUnaggreatedSamples,
  uint32_t      *maxDownSampleRatio,
  PS3000A_RATIO_MODE  downSampleRatioMode,
  uint32_t      segmentIndex
); """
make_symbol(ldlib, "GetMaxDownSampleRatio", "ps3000aGetMaxDownSampleRatio", c_uint32,
            [c_int16, c_uint32, c_void_p, c_int32, c_uint32])

""" PICO_STATUS ps3000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS3000a_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValues", "ps3000aGetValues", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps3000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesBulk", "ps3000aGetValuesBulk", c_uint32,
            [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p])

""" PICO_STATUS ps3000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
make_symbol(ldlib, "GetValuesAsync", "ps3000aGetValuesAsync", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps3000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlapped", "ps3000aGetValuesOverlapped", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps3000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlappedBulk", "ps3000aGetValuesOverlappedBulk", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p])

""" PICO_STATUS ps3000aGetTriggerInfoBulk
    (
        int16_t               handle,
        PS3000A_TRIGGER_INFO *triggerInfo,
        uint32_t              fromSegmentIndex,
        uint32_t              toSegmentIndex
    ); """
make_symbol(ldlib, "GetTriggerInfoBulk", "ps3000aGetTriggerInfoBulk", c_uint32, [c_int16, c_void_p, c_uint32, c_uint32])

""" PICO_STATUS ps3000aStop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps3000aStop", c_uint32, [c_int16, ])

""" PICO_STATUS ps3000aHoldOff
    (
        int16_t               handle,
        uint64_t              holdoff,
        PS3000A_HOLDOFF_TYPE  type
    ); """
make_symbol(ldlib, "HoldOff", "ps3000aHoldOff", c_uint32, [c_int16, c_uint64, c_int32])

""" PICO_STATUS ps3000aGetChannelInformation
    (
        int16_t               handle,
        PS3000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
make_symbol(ldlib, "GetChannelInformation", "ps3000aGetChannelInformation", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32])

""" PICO_STATUS ps3000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
make_symbol(ldlib, "EnumerateUnits", "ps3000aEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p])

""" PICO_STATUS ps3000aPingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps3000aPingUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps3000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
make_symbol(ldlib, "MaximumValue", "ps3000aMaximumValue", c_uint32, [c_int16, c_void_p])

"""" PICO_STATUS ps3000aMinimumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
make_symbol(ldlib, "MinimumValue", "ps3000aMinimumValue", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps3000aGetAnalogueOffset
    (
        int16_t           handle,
        PS3000A_RANGE     range,
        PS3000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
make_symbol(ldlib, "GetAnalogueOffset", "ps3000aGetAnalogueOffset", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p])

""" PICO_STATUS ps3000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
make_symbol(ldlib, "GetMaxSegments", "ps3000aGetMaxSegments", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps3000aChangePowerSource
    (
        int16_t     handle,
        PICO_STATUS powerState
    ); """
make_symbol(ldlib, "ChangePowerSource", "ps3000aChangePowerSource", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps3000aCurrentPowerSource
    (
        int16_t handle
    ); """
make_symbol(ldlib, "CurrentPowerSource", "ps3000aCurrentPowerSource", c_uint32, [c_int16, c_uint32])

"""
Defaults
"""
INI_LOGIC_VOLTS = 1.5


class BWLimit(dict2class):
    bw_full = 0
    bw_20MHz = 1

    def map(self):
        return [self.bw_full, self.bw_20MHz]

variants = ("3204A", "3204B", "3204MSO", "3205A", "3205B", "3205MSO",
            "3206A", "3206B", "3206MSO", "3207A", "3207B",
            "3404A", "3404B", "3405A", "3405B", "3406A", "3406B",
            "3204DMSO", "3205DMSO", "3206DMSO", "3404DMSO", "3405DMSO", "3406DMSO",
            "3203C", "3204C", "3205C", "3206C", "3203D", "3204D", "3205D", "3206D",
            "3403C", "3404C", "3405C", "3406C", "3403D", "3404D", "3405D", "3406D", )


class Device(PS5000Device):
    def __init__(self):
        self.m = sys.modules[__name__]
        super(Device, self).__init__(ldlib)

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
        self.info.handle = self._handle
        """ Read INFO from device, populate self.info """
        if status == pico_num("PICO_OK"):
            status = self.load_info()
        return status

    def load_info(self):
        """ Allows to continue loading after initial failure
        :returns: status of the call
        :rtype: int
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
        self.info.has_siggen = True
        self.info.siggen_frequency = 1000000
        self.info.siggen_min = 0
        self.info.siggen_max = 40000000
        if self.info.variant_info == "3204A":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = False
            self.info.awg_size = 1
            self.info.has_ets = False
        elif self.info.variant_info == "3204B":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 8192
            self.info.has_ets = False
        elif self.info.variant_info == "3204MSO":
            self.info.num_channels = 2
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 8192
            self.info.has_ets = False
        elif self.info.variant_info == "3205A":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = False
            self.info.awg_size = 1
            self.info.has_ets = True
        elif self.info.variant_info == "3205B":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 8192
            self.info.has_ets = True
        elif self.info.variant_info == "3205MSO":
            self.info.num_channels = 2
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 8192
            self.info.has_ets = True
        elif self.info.variant_info == "3206A":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = False
            self.info.awg_size = 1
            self.info.has_ets = True
        elif self.info.variant_info == "3206B":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 16384
            self.info.has_ets = True
        elif self.info.variant_info == "3206MSO":
            self.info.num_channels = 2
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 16384
            self.info.has_ets = True
        elif self.info.variant_info == "3207A":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = False
            self.info.awg_size = 1
            self.info.has_ets = True
        elif self.info.variant_info == "3207B":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3404A":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = False
            self.info.awg_size = 1
            self.info.has_ets = False
        elif self.info.variant_info == "3404B":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 8192
            self.info.has_ets = False
        elif self.info.variant_info == "3405A":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = False
            self.info.awg_size = 1
            self.info.has_ets = True
        elif self.info.variant_info == "3405B":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 8192
            self.info.has_ets = True
        elif self.info.variant_info == "3406A":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = False
            self.info.awg_size = 1
            self.info.has_ets = True
        elif self.info.variant_info == "3406B":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r50mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 16384
            self.info.has_ets = True
        elif self.info.variant_info == "3204DMSO":
            self.info.num_channels = 2
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3205DMSO":
            self.info.num_channels = 2
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3206DMSO":
            self.info.num_channels = 2
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3404DMSO":
            self.info.num_channels = 4
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3405DMSO":
            self.info.num_channels = 4
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3406DMSO":
            self.info.num_channels = 4
            self.info.num_ports = 2
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3203C":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3204C":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3205C":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3206C":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3203D":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3204D":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3205D":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3206D":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3403C":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3404C":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3405C":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3406C":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3403D":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3404D":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = True
        elif self.info.variant_info == "3405D":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
        elif self.info.variant_info == "3406D":
            self.info.num_channels = 4
            self.info.num_ports = 0
            self.info.min_range = self.m.Ranges.r20mv
            self.info.max_range = self.m.Ranges.r20v
            self.info.has_awg = True
            self.info.awg_size = 32768
            self.info.has_ets = False
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
            state = self.m.ChannelState()
            state.enabled = False
            state.coupling = self.m.Couplings.dc
            state.range = self.m.Ranges.r500mv
            state.offset = 0
            self.set_channel(Channels.map[channel], state)
        for port in range(0, self.info.num_ports):
            state = PortState()
            state.enabled = False
            state.level = INI_LOGIC_VOLTS
            self.set_digital_port(Ports.map[port], state)
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


def enumerate_units():
    global ldlib
    return ps5000base.enumerate_units(ldlib)
