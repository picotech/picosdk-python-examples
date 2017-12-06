#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps4000aApi.h C header
file for PicoScope 4000 Series oscilloscopes using the ps4000a driver API
functions.
"""

from ps5000base import *
from psutils import *
from picosdk import ps5000base

name = "ps4000a"
_libps4000a = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps4000a
ldlib.name = name

""" PICO_STATUS ps4000aOpenUnit
    (
        int16_t *handle,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnit", "ps4000aOpenUnit", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps4000aOpenUnitAsync
    (
        int16_t *status,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps4000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps4000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps4000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps4000aGetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t   *requiredSize,
        PICO_INFO  info
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps4000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps4000aFlashLed
    (
        int16_t  handle,
        int16_t  start
    ); """
make_symbol(ldlib, "FlashLed", "ps4000aFlashLed", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps4000aSetChannelLed
    (
        int16_t                      handle,
        PS4000A_CHANNEL_LED_SETTING *ledStates,
        uint16_t                     nLedStates
    ); """
make_symbol(ldlib, "SetChannelLed", "ps4000aSetChannelLed", c_uint32, [c_int16, c_void_p, c_uint16])

""" PICO_STATUS ps4000aIsLedFlashing
    (
        int16_t  handle,
        int16_t *status
    ); """
make_symbol(ldlib, "IsLedFlashing", "ps4000aIsLedFlashing", c_uint32, [c_int16, c_void_p, c_uint16])

""" PICO_STATUS ps4000aCloseUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps4000aCloseUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
make_symbol(ldlib, "MemorySegments", "ps4000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p])

""" PICO_STATUS ps4000aSetChannel
    (
        int16_t           handle,
        PS4000A_CHANNEL   channel,
        int16_t           enabled,
        PS4000A_COUPLING  type,
        PS4000A_RANGE     range,
        float             analogOffset
    ); """
make_symbol(ldlib, "SetChannel", "ps4000aSetChannel", c_uint32, [c_int16, c_int32, c_int16, c_int32, c_int32, c_float])

""" PICO_STATUS ps4000aSetBandwidthFilter
    (
        int16_t                    handle,
        PS4000A_CHANNEL            channel,
        PS4000A_BANDWIDTH_LIMITER  bandwidth
    ); """
make_symbol(ldlib, "SetBandwidthFilter", "ps4000aSetBandwidthFilter", c_uint32, [c_int16, c_int32, c_int32])

""" PICO_STATUS ps4000aApplyResistanceScaling
    (
        int16_t          handle,
        PS4000A_CHANNEL  channel,
        PS4000A_RANGE    range,
        int16_t         *bufferMax,
        int16_t         *bufferMin,
        uint32_t         buffertLth,
        int16_t         *overflow
    ); """
make_symbol(ldlib, "ApplyResistanceScaling", "ps4000aApplyResistanceScaling", c_uint32,
            [c_int16, c_int32, c_int32, c_int16, c_int16, c_uint32, c_int16])

""" PICO_STATUS ps4000aGetTimebase
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        int32_t  *timeIntervalNanoseconds,
        int32_t  *maxSamples,
        uint32_t  segmentIndex
    ); """

""" PICO_STATUS ps4000aGetTimebase2
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        float    *timeIntervalNanoseconds,
        int32_t  *maxSamples,
        uint32_t  segmentIndex
    ); """
make_symbol(ldlib, "GetTimebase", "ps4000aGetTimebase2", c_uint32,
            [c_int16, c_uint32, c_int32, c_void_p, c_void_p, c_uint32])

""" PICO_STATUS ps4000aSetSigGenArbitrary
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
        PS4000A_SWEEP_TYPE          sweepType,
        PS4000A_EXTRA_OPERATIONS    operation,
        PS4000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenArbitrary", "ps4000aSetSigGenArbitrary", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p,
             c_int32, c_int32, c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps4000aSetSigGenBuiltIn
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        PS4000A_WAVE_TYPE           waveType,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS4000A_SWEEP_TYPE          sweepType,
        PS4000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenBuiltIn", "ps4000aSetSigGenBuiltIn", c_uint32,
            [c_int16, c_int32, c_uint32, c_int32, c_double, c_double, c_double, c_double,
             c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps4000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS4000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesArbitrary", "ps4000aSetSigGenPropertiesArbitrary", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps4000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS4000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesBuiltIn", "ps4000aSetSigGenPropertiesBuiltIn", c_uint32,
            [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps4000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS4000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
make_symbol(ldlib, "SigGenFrequencyToPhase", "ps4000aSigGenFrequencyToPhase", c_uint32,
            [c_int16, c_double, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps4000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
make_symbol(ldlib, "SigGenArbitraryMinMaxValues", "ps4000aSigGenArbitraryMinMaxValues", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps4000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    );"""
make_symbol(ldlib, "SigGenSoftwareControl", "ps4000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps4000aSetEts
    (
        int16_t           handle,
        PS4000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
make_symbol(ldlib, "SetEts", "ps4000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

""" PICO_STATUS ps4000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS4000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetTriggerChannelProperties", "ps4000aSetTriggerChannelProperties", c_uint32,
            [c_int16, c_void_p, c_int16, c_int16, c_int32])

""" PICO_STATUS ps4000aSetTriggerChannelConditions
    (
        int16_t                  handle,
        PS4000A_CONDITION       *conditions,
        int16_t                  nConditions,
        PS4000A_CONDITIONS_INFO  info
    ); """
make_symbol(ldlib, "SetTriggerChannelConditions", "ps4000aSetTriggerChannelConditions", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32])

""" PICO_STATUS ps4000aSetTriggerChannelDirections
    (
        int16_t            handle,
        PS4000A_DIRECTION *directions,
        int16_t            nDirections
    ); """
make_symbol(ldlib, "SetTriggerChannelDirections", "ps4000aSetTriggerChannelDirections", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps4000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS4000A_CHANNEL              source,
        int16_t                      threshold,
        PS4000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
make_symbol(ldlib, "SetSimpleTrigger", "ps4000aSetSimpleTrigger", c_uint32,
            [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

""" PICO_STATUS ps4000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
make_symbol(ldlib, "SetTriggerDelay", "ps4000aSetTriggerDelay", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps4000aSetPulseWidthQualifierProperties
    (
        int16_t                      handle,
        PS4000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS4000A_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifierProperties", "ps4000aSetPulseWidthQualifierProperties", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps4000aSetPulseWidthQualifierConditions
    (
        int16_t                  handle,
        PS4000A_CONDITION       *conditions,
        int16_t                  nConditions,
        PS4000A_CONDITIONS_INFO  info
    ); """
make_symbol(ldlib, "SetPulseWidthQualifierConditions", "ps4000aSetPulseWidthQualifierConditions", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32])

""" PICO_STATUS ps4000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps4000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps4000aGetTriggerTimeOffset
    (
        int16_t             handle,
        uint32_t           *timeUpper,
        uint32_t           *timeLower,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """

""" PICO_STATUS ps4000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
make_symbol(ldlib, "GetTriggerTimeOffset", "ps4000aGetTriggerTimeOffset64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32])

""" PICO_STATUS ps4000aGetValuesTriggerTimeOffsetBulk
    (
        int16_t             handle,
        uint32_t           *timesUpper,
        uint32_t           *timesLower,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """

""" PICO_STATUS ps4000aGetValuesTriggerTimeOffsetBulk64
    (
        int16_t             handle,
        int64_t            *times,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps4000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32, c_uint32])

""" PICO_STATUS ps4000aSetDataBuffers
    (
        int16_t             handle,
        PS4000A_CHANNEL     channel,
        int16_t            *bufferMax,
        int16_t            *bufferMin,
        int32_t             bufferLth,
        uint32_t            segmentIndex,
        PS4000A_RATIO_MODE  mode
    ); """
make_symbol(ldlib, "SetDataBuffers", "ps4000aSetDataBuffers", c_uint32,
            [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps4000aSetDataBuffer
    (
        int16_t             handle,
        PS4000A_CHANNEL     channel,
        int16_t            *buffer,
        int32_t             bufferLth,
        uint32_t            segmentIndex,
        PS4000A_RATIO_MODE  mode
    ); """
make_symbol(ldlib, "SetDataBuffer", "ps4000aSetDataBuffer", c_uint32,
            [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32])

""" PICO_STATUS ps4000aSetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffer", "ps4000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32])

""" PICO_STATUS ps4000aSetEtsTimeBuffers
    (
        int16_t   handle,
        uint32_t *timeUpper,
        uint32_t *timeLower,
        int32_t   bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffers", "ps4000aSetEtsTimeBuffers", c_uint32, [c_int16, c_void_p, c_void_p, c_int32])

""" PICO_STATUS ps4000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
make_symbol(ldlib, "IsReady", "ps4000aIsReady", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps4000aBlockReady  lpReady,
        void              *pParameter
    ); """
make_symbol(ldlib, "RunBlock", "ps4000aRunBlock", c_uint32,
            [c_int16, c_int32, c_int32, c_uint32, c_void_p, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps4000aRunStreaming
    (
        int16_t             handle,
        uint32_t           *sampleInterval,
        PS4000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
make_symbol(ldlib, "RunStreaming", "ps4000aRunStreaming", c_uint32,
            [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32])

""" PICO_STATUS ps4000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps4000aStreamingReady  lpPs4000aReady,
        void                  *pParameter
    ); """
make_symbol(ldlib, "GetStreamingLatestValues", "ps4000aGetStreamingLatestValues", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps4000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
make_symbol(ldlib, "NoOfStreamingValues", "ps4000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aGetMaxDownSampleRatio
    (
        int16_t             handle,
        uint32_t            noOfUnaggreatedSamples,
        uint32_t           *maxDownSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex
    ); """
make_symbol(ldlib, "GetMaxDownSampleRatio", "ps4000aGetMaxDownSampleRatio", c_uint32,
            [c_int16, c_uint32, c_void_p, c_int32, c_uint32])

""" PICO_STATUS ps4000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValues", "ps4000aGetValues", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps4000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
make_symbol(ldlib, "GetValuesAsync", "ps4000aGetValuesAsync", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps4000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesBulk", "ps4000aGetValuesBulk", c_uint32,
            [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p])

""" PICO_STATUS ps4000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlapped", "ps4000aGetValuesOverlapped", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps4000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlappedBulk", "ps4000aGetValuesOverlappedBulk", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p])

""" PICO_STATUS ps4000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
make_symbol(ldlib, "EnumerateUnits", "ps4000aEnumerateUnits", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps4000aGetChannelInformation
    (
        int16_t               handle,
        PS4000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
make_symbol(ldlib, "GetChannelInformation", "ps4000aGetChannelInformation", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32])

""" PICO_STATUS ps4000aConnectDetect
    (
        int16_t                 handle,
        PS4000A_CONNECT_DETECT *sensor,
        int16_t                 nSensors
    ); """
make_symbol(ldlib, "ConnectDetect", "ps4000aConnectDetect", c_uint32, [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps4000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
make_symbol(ldlib, "MaximumValue", "ps4000aMaximumValue", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aMinimumValue
    (
        int16_t		handle,
        int16_t * value
    ); """
make_symbol(ldlib, "MinimumValue", "ps4000aMinimumValue", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aGetAnalogueOffset
    (
        int16_t           handle,
        PS4000A_RANGE     range,
        PS4000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
make_symbol(ldlib, "GetAnalogueOffset", "ps4000aGetAnalogueOffset", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p])

""" PICO_STATUS ps4000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
make_symbol(ldlib, "GetMaxSegments", "ps4000aGetMaxSegments", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aChangePowerSource
    (
        int16_t      handle,
        PICO_STATUS  powerState
    ); """
make_symbol(ldlib, "ChangePowerSource", "ps4000aChangePowerSource", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps4000aCurrentPowerSource
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "CurrentPowerSource", "ps4000aCurrentPowerSource", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000aStop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps4000aStop", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000aPingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps4000aPingUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps4000aSetNoOfCaptures
    (
        int16_t   handle,
        uint32_t  nCaptures
    ); """
make_symbol(ldlib, "SetNoOfCaptures", "ps4000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps4000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
make_symbol(ldlib, "GetNoOfCaptures", "ps4000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aGetNoOfProcessedCaptures
    (
        int16_t   handle,
        uint32_t *nProcessedCaptures
    ); """
make_symbol(ldlib, "GetNoOfProcessedCaptures", "ps4000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aDeviceMetaData
    (
        int16_t                 handle,
        int8_t                 *settings,
        int32_t                *nSettingsLength,
        PS4000A_META_TYPE       type,
        PS4000A_META_OPERATION  operation,
        PS4000A_META_FORMAT     format
    ); """
make_symbol(ldlib, "DeviceMetaData", "ps4000aDeviceMetaData", c_uint32,
            [c_int16, c_void_p, c_void_p, c_int32, c_int32, c_int32])

""" PICO_STATUS ps4000aGetString
    (
        int16_t            handle,
        PICO_STRING_VALUE  stringValue,
        int8_t            *string,
        int32_t           *stringLength
    ); """
make_symbol(ldlib, "GetString", "ps4000aGetString", c_uint32, [c_int16, c_int32, c_void_p, c_void_p])

""" PICO_STATUS ps4000aGetCommonModeOverflow
    (
        int16_t   handle,
        uint16_t *overflow
    ); """
make_symbol(ldlib, "GetCommonModeOverflow", "ps4000aGetCommonModeOverflow", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps4000aSetFrequencyCounter
    (
        int16_t                          handle,
        PS4000A_CHANNEL                  channel,
        int16_t                          enabled,
        PS4000A_FREQUENCY_COUNTER_RANGE  range,
        int16_t                          thresholdMajor,
        int16_t                          thresholdMinor
    ); """
make_symbol(ldlib, "SetFrequencyCounter", "ps4000aSetFrequencyCounter", c_uint32,
            [c_int16, c_int32, c_int16, c_int32, c_int16, c_int16])


class Channels(ps5000base.Channels):
    """ Class defining channels for the current device class """
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    map = (A, B, C, D, E, F, G, H)
    labels = {A: "A", B: "B", C: "C", D: "D", E: "E", F: "F", G: "G", H: "H"}


class TriggerChannels(ps5000base.TriggerChannels):
    """ Collection of channels used in triggering """
    A = Channels.A
    B = Channels.B
    C = Channels.C
    D = Channels.D
    E = Channels.E
    F = Channels.F
    G = Channels.G
    H = Channels.H
    Ext = 8
    Aux = 9
    Pwq = 0x10000000
    map = (A, B, C, D, E, F, G, H, Ext, Aux, Pwq)
    labels = {A: "A", B: "B", C: "C", D: "D", E: "E", F: "F", G: "G", H: "H", Ext: "EXT", Aux: "AUX", Pwq: "PWQ"}


class TriggerDirectionStruct(Structure):
    """ Ctype specifier for Trigger Direction structure in Advanced Trigger """
    _fields_ = [
        ("channel", c_int32),
        ("direction", c_int32),
    ]
    _pack_ = 1


class TriggerDirection(dict2class):
    """ Trigger direction object specifier """
    channel = TriggerChannels.A
    direction = ThresholdDirections.none

    def to_struct(self):
        return TriggerDirectionStruct(self.channel, self.direction)


class TriggerConditionsStruct(Structure):
    """ CType specifier for Trigger Conditions """
    _fields_ = [
        ("channel", c_int32),
        ("state", c_int32),
    ]
    _pack_ = 1


class TriggerConditions(ps5000base.TriggerConditions):
    """ Collection of Trigger Conditions for Advanced Triggering """
    chA = TriggerState.dont_care
    chB = TriggerState.dont_care
    chC = TriggerState.dont_care
    chD = TriggerState.dont_care
    chE = TriggerState.dont_care
    chF = TriggerState.dont_care
    chG = TriggerState.dont_care
    chH = TriggerState.dont_care
    ext = TriggerState.dont_care
    aux = TriggerState.dont_care
    pwq = TriggerState.dont_care

    def to_struct(self):
        return None

    def is_set(self):
        return len([c for c in
                    (self.chA, self.chB, self.chC, self.chD,
                     self.chE, self.chF, self.chG, self.chH,
                     self.ext, self.aux, self.pwq)
                    if c != TriggerState.dont_care]) > 0

    def to_trigger_channels(self):
        return {
            TriggerChannels.A: self.chA,
            TriggerChannels.B: self.chB,
            TriggerChannels.C: self.chC,
            TriggerChannels.D: self.chD,
            TriggerChannels.E: self.chE,
            TriggerChannels.F: self.chF,
            TriggerChannels.G: self.chG,
            TriggerChannels.H: self.chH,
            TriggerChannels.Ext: self.ext,
            TriggerChannels.Aux: self.aux,
            TriggerChannels.Pwq: self.pwq,
        }


class TriggerConditionInfo(dict2class):
    clear = 1
    add = 2


class PwqConditions(ps5000base.PwqConditions):
    """ Collection of Pulse Width Qualifier Conditions """
    chA = TriggerState.dont_care
    chB = TriggerState.dont_care
    chC = TriggerState.dont_care
    chD = TriggerState.dont_care
    chE = TriggerState.dont_care
    chF = TriggerState.dont_care
    chG = TriggerState.dont_care
    chH = TriggerState.dont_care
    ext = TriggerState.dont_care
    aux = TriggerState.dont_care

    def to_struct(self):
        return None

    def is_set(self):
        return len([c for c in
                    (self.chA, self.chB, self.chC, self.chD,
                     self.chE, self.chF, self.chG, self.chH,
                     self.ext, self.aux)
                    if c != TriggerState.dont_care]) > 0

    def to_trigger_channels(self):
        return {
            TriggerChannels.A: self.chA,
            TriggerChannels.B: self.chB,
            TriggerChannels.C: self.chC,
            TriggerChannels.D: self.chD,
            TriggerChannels.E: self.chE,
            TriggerChannels.F: self.chF,
            TriggerChannels.G: self.chG,
            TriggerChannels.H: self.chH,
            TriggerChannels.Ext: self.ext,
            TriggerChannels.Aux: self.aux,
        }

variants = ("4824", "4424", "4425", "4225")


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
        self.info.has_awg = False
        if self.info.variant_info == "4824":
            self.info.num_channels = 8
            self.info.min_range = Ranges.r10mv
            self.info.max_range = Ranges.r50v
            self.info.has_siggen = True
            self.info.siggen_frequency = 1000000
            self.info.siggen_min = 0
            self.info.siggen_max = 4000000
            self.info.has_awg = True
            self.info.awg_size = 16384
            self.info.has_ets = True
        elif self.info.variant_info == "4424":
            self.info.num_channels = 4
            self.info.min_range = Ranges.r10mv
            self.info.max_range = Ranges.r50v
            self.info.has_siggen = True
            self.info.siggen_frequency = 1000000
            self.info.siggen_min = 0
            self.info.siggen_max = 4000000
            self.info.has_awg = True
            self.info.awg_size = 16384
            self.info.has_ets = True
        elif self.info.variant_info == "4425":
            self.info.num_channels = 4
            self.info.min_range = Ranges.r50mv
            self.info.max_range = Ranges.r200v
            self.info.has_siggen = False
            self.info.has_awg = False
            self.info.has_ets = False
        elif self.info.variant_info == "4225":
            self.info.num_channels = 2
            self.info.min_range = Ranges.r50mv
            self.info.max_range = Ranges.r200v
            self.info.has_siggen = False
            self.info.has_awg = False
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

    def set_advanced_trigger(self, conditions=None, analog=None, digital=None, waitfor=0):
        """ Passes advanced triggering setup to the driver
        :param conditions: tuple of TriggerConditions objects, they are joined by OR operand. None to turn off
        :type conditions: tuple, None
        :param analog: tuple of TriggerChannelProperties objects, None to ignore all
        :type analog: tuple, None
        :param digital: None, not used
        :type digital: None
        :param waitfor: time in miliseconds, how long to wait for trigger to occur. If 0 - indefinitely
        :param waitfor: int
        :return: final status of subsequent calls
        :rtype: int
        """
        if self._handle <= 0:
            return pico_num("PICO_INVALID_HANDLE")

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
        analogdir = ()
        if len(analog) > 0:
            # scan and discards duplicates
            triggchans = ()
            for p in analog:
                if not isinstance(p, self.m.TriggerChannelProperties) or p.channel not in self.m.TriggerChannels.map:
                    continue
                if p.channel not in triggchans:
                    triggchans += (p.channel,)

                    if p.direction in self.m.ThresholdDirections.map:
                        analogdir += (self.m.TriggerDirection(channel=p.channel, direction=p.direction),)
                    else:
                        analogdir += \
                            (self.m.TriggerDirection(channel=p.channel, direction=self.m.ThresholdDirections.none))
                    analogout += (p,)
        if len(analogout) > 0:
            analogprops = cast(((self.m.TriggerChannelPropertiesStruct * len(analogout))()),
                               POINTER(self.m.TriggerChannelPropertiesStruct))
            for i in range(0, len(analogout)):
                analogprops[i] = analogout[i].to_struct()
        else:
            analogprops = None

        if len(analogdir) > 0:
            dirs = cast(((self.m.TriggerDirectionStruct * len(analogdir))()), POINTER(self.m.TriggerDirectionStruct))
            for i in range(0, len(analogdir)):
                dirs[i] = analogdir[i].to_struct()
        else:
            dirs = None

        status = ldlib.SetTriggerChannelDirections(self._chandle, dirs, c_int16(len(analogdir)))
        if status != pico_num("PICO_OK"):
            return status

        status = ldlib.SetTriggerChannelProperties(
            self._chandle, analogprops, c_int16(len(analogout)), c_int16(0), c_int32(waitfor))
        if status != pico_num("PICO_OK"):
            return status
        # finally do the conditions
        conditionsout = ()
        if len(conditions) > 0:
            for c in conditions:
                if not isinstance(c, self.m.TriggerConditions) or not c.is_set():
                    continue
                conditionsout += (c,)
        # clear existing conditions
        status = ldlib.SetTriggerChannelConditions(self._chandle, None, c_int16(0),
                                                   c_int32(self.m.TriggerConditionInfo.clear))
        if status != pico_num("PICO_OK"):
            return status
        for c in conditionsout:
            tcs = c.to_trigger_channels()
            conds = cast(((self.m.TriggerConditionsStruct * len(tcs))()), POINTER(self.m.TriggerConditionsStruct))
            for i in range(0, len(tcs)):
                chann = self.m.TriggerChannels.map[i]
                conds[i].channel = chann
                conds[i].state = tcs[chann]
            status = ldlib.SetTriggerChannelConditions(self._chandle, conds, c_int16(len(tcs)),
                                                       c_int32(TriggerConditionInfo.add))
            if status != pico_num("PICO_OK"):
                return status

        self.trigger_conditions = conditionsout
        self.trigger_analog = analogout
        self.trigger_digital = None
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

        conditionsout = ()
        for c in conditions:
            if not isinstance(c, self.m.PwqConditions) or not c.is_set():
                continue
            conditionsout += (c,)
        if len(conditionsout) == 0:
            conditionsout += (self.m.PwqConditions(),)
        # clear existing conditions
        status = ldlib.SetPulseWidthQualifierConditions(self._chandle, None, c_int16(0),
                                                        c_int32(self.m.TriggerConditionInfo.clear))
        if status != pico_num("PICO_OK"):
            return status
        if len(conditionsout) > 0:
            status = ldlib.SetPulseWidthQualifierProperties(self._chandle, c_int32(direction),
                                                            c_uint32(lower), c_uint32(upper), c_int32(pwqtype))
            if status != pico_num("PICO_OK"):
                return status
            for c in conditionsout:
                tcs = c.to_trigger_channels()
                conds = cast(((self.m.TriggerConditionsStruct * len(tcs))()), POINTER(self.m.TriggerConditionsStruct))
                for i in range(0, len(tcs)):
                    chann = self.m.TriggerChannels.map[i]
                    conds[i].channel = chann
                    conds[i].state = tcs[chann]
                status = ldlib.SetPulseWidthQualifierConditions(self._chandle, conds, c_int16(len(tcs)),
                                                                c_int32(self.m.TriggerConditionInfo.clear))
                if status != pico_num("PICO_OK"):
                    return status

        self.pwq_conditions = conditionsout
        self.pwq_direction = direction
        self.pwq_lower = lower
        self.pwq_upper = upper
        self.pwq_type = pwqtype
        return pico_num("PICO_OK")

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
