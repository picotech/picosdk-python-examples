#
# Copyright (C) 2014-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Python bindings for [lib]ps2000a.[dll|so|dylib]
This is a Python module defining the functions from the ps2000aApi.h C header
file for PicoScope 2000 Series oscilloscopes using the ps2000a driver API functions.
"""

from ps5000base import *
from psutils import *
from picosdk import ps5000base

name = "ps2000a"
_libps2000a = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps2000a
ldlib.name = name

""" PICO_STATUS ps2000aOpenUnit
    (
        int16_t *status,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnit", "ps2000aOpenUnit", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps2000aOpenUnitAsync
    (
        int16_t *status,
        int8_t	*serial
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps2000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps2000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps2000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps2000aGetUnitInfo
    (
        int16_t   handle,
        int8_t   *string,
        int16_t   stringLength,
        int16_t  *requiredSize,
        PICO_INFO info
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps2000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps2000aFlashLed
    (
        int16_t handle,
        int16_t start
    ); """
make_symbol(ldlib, "FlashLed", "ps2000aFlashLed", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps2000aCloseUnit
    (
        int16_t handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps2000aCloseUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps2000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
make_symbol(ldlib, "MemorySegments", "ps2000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p])

""" PICO_STATUS ps2000aSetChannel
    (
        int16_t          handle,
        PS2000A_CHANNEL  channel,
        int16_t          enabled,
        PS2000A_COUPLING type,
        PS2000A_RANGE    range,
        float            analogOffset
    ); """
make_symbol(ldlib, "SetChannel", "ps2000aSetChannel", c_uint32, [c_int16, c_int32, c_int16, c_int32, c_int32, c_float])

""" PICO_STATUS ps2000aSetDigitalPort
    (
        int16_t              handle,
        PS2000A_DIGITAL_PORT port,
        int16_t              enabled,
        int16_t              logicLevel
    ); """
make_symbol(ldlib, "SetDigitalPort", "ps2000aSetDigitalPort", c_uint32, [c_int16, c_int32, c_int16, c_int16])

""" PICO_STATUS ps2000aSetNoOfCaptures
    (
        int16_t  handle,
        uint32_t nCaptures
    ); """
make_symbol(ldlib, "SetNoOfCaptures", "ps2000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps2000aGetTimebase2
    (
        int16_t  handle,
        uint32_t timebase,
        int32_t  noSamples,
        float   *timeIntervalNanoseconds,
        int16_t  oversample,
        int32_t *maxSamples,
        uint32_t segmentIndex
    ); """
make_symbol(ldlib, "GetTimebase", "ps2000aGetTimebase2", c_uint32,
            [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps2000aSetSigGenArbitrary
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
        PS2000A_SWEEP_TYPE          sweepType,
        PS2000A_EXTRA_OPERATIONS    operation,
        PS2000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenArbitrary", "ps2000aSetSigGenArbitrary", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32, c_int32,
             c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps2000aSetSigGenBuiltIn
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        int16_t                     waveType,
        float                       startFrequency,
        float                       stopFrequency,
        float                       increment,
        float                       dwellTime,
        PS2000A_SWEEP_TYPE          sweepType,
        PS2000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenBuiltIn", "ps2000aSetSigGenBuiltIn", c_uint32,
            [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float, c_int32, c_int32, c_uint32,
             c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps2000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS2000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesArbitrary", "ps2000aSetSigGenPropertiesArbitrary", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps2000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS2000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesBuiltIn", "ps2000aSetSigGenPropertiesBuiltIn", c_uint32,
            [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps2000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS2000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
make_symbol(ldlib, "SigGenFrequencyToPhase", "ps2000aSigGenFrequencyToPhase", c_uint32,
            [c_int16, c_double, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps2000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
make_symbol(ldlib, "SigGenArbitraryMinMaxValues", "ps2000aSigGenArbitraryMinMaxValues", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps2000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "SigGenSoftwareControl", "ps2000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps2000aSetEts
    (
        int16_t           handle,
        PS2000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
make_symbol(ldlib, "SetEts", "ps2000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

""" PICO_STATUS ps2000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS2000A_CHANNEL              source,
        int16_t                      threshold,
        PS2000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
make_symbol(ldlib, "SetSimpleTrigger", "ps2000aSetSimpleTrigger", c_uint32,
            [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

""" PICO_STATUS ps2000aSetTriggerDigitalPortProperties
    (
        int16_t                             handle,
        PS2000A_DIGITAL_CHANNEL_DIRECTIONS *directions,
        int16_t                             nDirections
    ); """
make_symbol(ldlib, "SetTriggerDigitalPortProperties", "ps2000aSetTriggerDigitalPortProperties", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps2000aSetDigitalAnalogTriggerOperand
    (
        int16_t handle,
        PS2000A_TRIGGER_OPERAND operand
    ); """
make_symbol(ldlib, "SetDigitalAnalogTriggerOperand", "ps2000aSetDigitalAnalogTriggerOperand", c_uint32,
            [c_int16, c_int32])

""" PICO_STATUS ps2000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS2000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetTriggerChannelProperties", "ps2000aSetTriggerChannelProperties", c_uint32,
            [c_int16, c_void_p, c_int16, c_int16, c_int32])

""" PICO_STATUS ps2000aSetTriggerChannelConditions
    (
        int16_t                     handle,
        PS2000A_TRIGGER_CONDITIONS *conditions,
        int16_t                     nConditions
    ); """
make_symbol(ldlib, "SetTriggerChannelConditions", "ps2000aSetTriggerChannelConditions", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps2000aSetTriggerChannelDirections
    (
        int16_t                      handle,
        PS2000A_THRESHOLD_DIRECTION  channelA,
        PS2000A_THRESHOLD_DIRECTION  channelB,
        PS2000A_THRESHOLD_DIRECTION  channelC,
        PS2000A_THRESHOLD_DIRECTION  channelD,
        PS2000A_THRESHOLD_DIRECTION  ext,
        PS2000A_THRESHOLD_DIRECTION  aux
    ); """
make_symbol(ldlib, "SetTriggerChannelDirections", "ps2000aSetTriggerChannelDirections", c_uint32,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32])

""" PICO_STATUS ps2000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
make_symbol(ldlib, "SetTriggerDelay", "ps2000aSetTriggerDelay", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps2000aSetPulseWidthQualifier
    (
        int16_t                      handle,
        PS2000A_PWQ_CONDITIONS      *conditions,
        int16_t                      nConditions,
        PS2000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS2000A_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifier", "ps2000aSetPulseWidthQualifier", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps2000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps2000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps2000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS2000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
make_symbol(ldlib, "GetTriggerTimeOffset", "ps2000aGetTriggerTimeOffset64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32])

""" PICO_STATUS PREF2 PREF3 (ps2000aGetValuesTriggerTimeOffsetBulk64)
    (
        int16_t             handle,
        int64_t            *times,
        PS2000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps2000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32, c_uint32])

""" PICO_STATUS ps2000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
make_symbol(ldlib, "GetNoOfCaptures", "ps2000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps2000aGetNoOfProcessedCaptures
    (
        int16_t   handle,
        uint32_t *nProcessedCaptures
    ); """
make_symbol(ldlib, "GetNoOfProcessedCaptures", "ps2000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps2000aSetDataBuffer
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *buffer,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS2000A_RATIO_MODE mode
    ); """
make_symbol(ldlib, "SetDataBuffer", "ps2000aSetDataBuffer", c_uint32,
            [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps2000aSetDataBuffers
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS2000A_RATIO_MODE mode
    ); """
make_symbol(ldlib, "SetDataBuffers", "ps2000aSetDataBuffers", c_uint32,
            [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps2000aSetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffer", "ps2000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32])

""" PICO_STATUS ps2000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
make_symbol(ldlib, "IsReady", "ps2000aIsReady", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps2000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int16_t            oversample,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps2000aBlockReady  lpReady,
        void              *pParameter
    ); """
make_symbol(ldlib, "RunBlock", "ps2000aRunBlock", c_uint32,
            [c_int16, c_int32, c_int32, c_uint32, c_int16, c_void_p, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps2000aRunStreaming
    (
        int16_t             handle,
        uint32_t            *sampleInterval,
        PS2000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostPreTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
make_symbol(ldlib, "RunStreaming", "ps2000aRunStreaming", c_uint32,
            [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32])

""" PICO_STATUS ps2000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps2000aStreamingReady  lpPs2000aReady,
        void                   *pParameter
    ); """
make_symbol(ldlib, "GetStreamingLatestValues", "ps2000aGetStreamingLatestValues", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" void *ps2000aStreamingReady
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

""" PICO_STATUS ps2000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
make_symbol(ldlib, "NoOfStreamingValues", "ps2000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps2000aGetMaxDownSampleRatio
    (
        int16_t             handle,
        uint32_t            noOfUnaggreatedSamples,
        uint32_t           *maxDownSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex
    ); """
make_symbol(ldlib, "GetMaxDownSampleRatio", "ps2000aGetMaxDownSampleRatio", c_uint32,
            [c_int16, c_uint32, c_void_p, c_int32, c_uint32])

""" PICO_STATUS ps2000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValues", "ps2000aGetValues", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps2000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesBulk", "ps2000aGetValuesBulk", c_uint32,
            [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p])

""" PICO_STATUS ps2000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
make_symbol(ldlib, "GetValuesAsync", "ps2000aGetValuesAsync", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps2000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlapped", "ps2000aGetValuesOverlapped", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps2000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlappedBulk", "ps2000aGetValuesOverlappedBulk", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_int32, c_void_p])

""" PICO_STATUS ps2000aStop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps2000aStop", c_uint32, [c_int16, ])

""" PICO_STATUS ps2000aHoldOff
    (
        int16_t               handle,
        uint64_t              holdoff,
        PS2000A_HOLDOFF_TYPE  type
    ); """
make_symbol(ldlib, "HoldOff", "ps2000aHoldOff", c_uint32, [c_int16, c_uint64, c_int32])

""" PICO_STATUS ps2000aGetChannelInformation
    (
        int16_t               handle,
        PS2000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
make_symbol(ldlib, "GetChannelInformation", "ps2000aGetChannelInformation", c_uint32,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32])

""" PICO_STATUS ps2000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
make_symbol(ldlib, "EnumerateUnits", "ps2000aEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p])

""" PICO_STATUS ps2000aPingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps2000aPingUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps2000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
make_symbol(ldlib, "MaximumValue", "ps2000aMaximumValue", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps2000aMinimumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
make_symbol(ldlib, "MinimumValue", "ps2000aMinimumValue", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps2000aGetAnalogueOffset
    (
        int16_t           handle,
        PS2000A_RANGE     range,
        PS2000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
make_symbol(ldlib, "GetAnalogueOffset", "ps2000aGetAnalogueOffset", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p])

""" PICO_STATUS ps2000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
make_symbol(ldlib, "GetMaxSegments", "ps2000aGetMaxSegments", c_uint32, [c_int16, c_void_p])

"""
Defaults
"""
INI_LOGIC_VOLTS = 1.5
variants = ("2205MSO", "2206", "2206A", "2207", "2207A", "2208", "2208A")


class Device(PS5000Device):
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
        self.info.min_range = self.m.Ranges.r50mv
        self.info.max_range = self.m.Ranges.r20v
        self.info.has_siggen = True
        self.info.siggen_frequency = 1000000
        self.info.siggen_min = 0
        self.info.siggen_max = 40000000
        self.info.has_awg = True
        self.info.has_ets = False
        if self.info.variant_info == "2205MSO":
            self.info.num_channels = 2
            self.info.num_ports = 2
            self.info.awg_size = 8192
        elif self.info.variant_info == "2206":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.awg_size = 8192
        elif self.info.variant_info == "2206A":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.awg_size = 8192
        elif self.info.variant_info == "2207":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.awg_size = 8192
        elif self.info.variant_info == "2207A":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.awg_size = 8192
        elif self.info.variant_info == "2208":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.awg_size = 8192
        elif self.info.variant_info == "2208A":
            self.info.num_channels = 2
            self.info.num_ports = 0
            self.info.awg_size = 8192
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
            self.set_channel(self.m.Channels.map[channel], state)
        for port in range(0, self.info.num_ports):
            state = self.m.PortState()
            state.enabled = False
            state.level = INI_LOGIC_VOLTS
            self.set_digital_port(self.m.Ports.map[port], state)
        return pico_num("PICO_OK")


def enumerate_units():
    global ldlib
    return ps5000base.enumerate_units(ldlib)
