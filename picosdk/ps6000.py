# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps6000Api.h C header
file for PicoScope 6000 Series oscilloscopes using the ps6000 driver API
functions.
"""

from ps5000base import *
from psutils import *
from picosdk import ps5000base

name = "ps6000"
_libps6000 = psloadlib(name)

""" ctypes bindings with helper-defaults"""
ldlib = dict2class()
ldlib.lib = _libps6000
ldlib.name = name

""" PICO_STATUS ps6000OpenUnit
    (
        int16_t *handle,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnit", "ps6000OpenUnit", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps6000OpenUnitAsync
    (
        int16_t *status,
        int8_t  *serial
    ); """
make_symbol(ldlib, "OpenUnitAsync", "ps6000OpenUnitAsync", c_uint32, [c_void_p, c_char_p])

""" PICO_STATUS ps6000OpenUnitProgress
    (
      int16_t *handle,
      int16_t *progressPercent,
      int16_t *complete
    ); """
make_symbol(ldlib, "OpenUnitProgress", "ps6000OpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps6000GetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t   *requiredSize,
        PICO_INFO  info
    ); """
make_symbol(ldlib, "GetUnitInfo", "ps6000GetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps6000FlashLed
    (
        int16_t  handle,
        int16_t  start
    ); """
make_symbol(ldlib, "FlashLed", "ps6000FlashLed", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps6000CloseUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "CloseUnit", "ps6000CloseUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps6000MemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        uint32_t *nMaxSamples
    ); """
make_symbol(ldlib, "MemorySegments", "ps6000MemorySegments", c_uint32, [c_int16, c_uint32, c_void_p])

""" PICO_STATUS ps6000SetChannel
    (
        int16_t                   handle,
        PS6000_CHANNEL            channel,
        int16_t                   enabled,
        PS6000_COUPLING           type,
        PS6000_RANGE              range,
        float                     analogueOffset,
        PS6000_BANDWIDTH_LIMITER  bandwidth
    ); """
make_symbol(ldlib, "SetChannel", "ps6000SetChannel", c_uint32,
            [c_int16, c_int32, c_int16, c_int32, c_int32, c_float, c_int32])

""" PICO_STATUS ps6000GetTimebase
    (
        int16_t   handle,
        uint32_t  timebase,
        uint32_t  noSamples,
        int32_t  *timeIntervalNanoseconds,
        int16_t   oversample,
        uint32_t *maxSamples,
        uint32_t  segmentIndex
    ); """

""" PICO_STATUS ps6000GetTimebase2
    (
        int16_t   handle,
        uint32_t  timebase,
        uint32_t  noSamples,
        float    *timeIntervalNanoseconds,
        int16_t   oversample,
        uint32_t *maxSamples,
        uint32_t  segmentIndex
    ); """
make_symbol(ldlib, "GetTimebase", "ps6000GetTimebase2", c_uint32,
            [c_int16, c_uint32, c_uint32, c_void_p, c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps6000SetSigGenArbitrary
    (
        int16_t                    handle,
        int32_t                    offsetVoltage,
        uint32_t                   pkToPk,
        uint32_t                   startDeltaPhase,
        uint32_t                   stopDeltaPhase,
        uint32_t                   deltaPhaseIncrement,
        uint32_t                   dwellCount,
        int16_t                   *arbitraryWaveform,
        int32_t                    arbitraryWaveformSize,
        PS6000_SWEEP_TYPE          sweepType,
        PS6000_EXTRA_OPERATIONS    operation,
        PS6000_INDEX_MODE          indexMode,
        uint32_t                   shots,
        uint32_t                   sweeps,
        PS6000_SIGGEN_TRIG_TYPE    triggerType,
        PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                    extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenArbitrary", "ps6000SetSigGenArbitrary", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p,
             c_int32, c_int32, c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps6000SetSigGenBuiltIn
    (
        int16_t                    handle,
        int32_t                    offsetVoltage,
        uint32_t                   pkToPk,
        int16_t                    waveType,
        float                      startFrequency,
        float                      stopFrequency,
        float                      increment,
        float                      dwellTime,
        PS6000_SWEEP_TYPE          sweepType,
        PS6000_EXTRA_OPERATIONS    operation,
        uint32_t                   shots,
        uint32_t                   sweeps,
        PS6000_SIGGEN_TRIG_TYPE    triggerType,
        PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                    extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenBuiltIn", "ps6000SetSigGenBuiltIn", c_uint32,
            [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float,
             c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps6000SetSigGenBuiltInV2
    (
        int16_t                    handle,
        int32_t                    offsetVoltage,
        uint32_t                   pkToPk,
        int16_t                    waveType,
        double                     startFrequency,
        double                     stopFrequency,
        double                     increment,
        double                     dwellTime,
        PS6000_SWEEP_TYPE          sweepType,
        PS6000_EXTRA_OPERATIONS    operation,
        uint32_t                   shots,
        uint32_t                   sweeps,
        PS6000_SIGGEN_TRIG_TYPE    triggerType,
        PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                    extInThreshold
    ); """

""" PICO_STATUS ps6000SetSigGenPropertiesArbitrary
    (
        int16_t                    handle,
        int32_t                    offsetVoltage,
        uint32_t                   pkToPk,
        uint32_t                   startDeltaPhase,
        uint32_t                   stopDeltaPhase,
        uint32_t                   deltaPhaseIncrement,
        uint32_t                   dwellCount,
        PS6000_SWEEP_TYPE          sweepType,
        uint32_t                   shots,
        uint32_t                   sweeps,
        PS6000_SIGGEN_TRIG_TYPE    triggerType,
        PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                    extInThreshold
    ); """
make_symbol(ldlib, "SigGenPropertiesArbitrary", "ps6000SetSigGenPropertiesArbitrary", c_uint32,
            [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32,
             c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps6000SetSigGenPropertiesBuiltIn
    (
        int16_t                    handle,
        int32_t                    offsetVoltage,
        uint32_t                   pkToPk,
        double                     startFrequency,
        double                     stopFrequency,
        double                     increment,
        double                     dwellTime,
        PS6000_SWEEP_TYPE          sweepType,
        uint32_t                   shots,
        uint32_t                   sweeps,
        PS6000_SIGGEN_TRIG_TYPE    triggerType,
        PS6000_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                    extInThreshold
    ); """
make_symbol(ldlib, "SetSigGenPropertiesBuiltIn", "ps6000SetSigGenPropertiesBuiltIn", c_uint32,
            [c_int16, c_int32, c_uint32, c_double, c_double, c_double, c_double,
             c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16])

""" PICO_STATUS ps6000SigGenFrequencyToPhase
    (
        int16_t            handle,
        double             frequency,
        PS6000_INDEX_MODE  indexMode,
        uint32_t           bufferLength,
        uint32_t          *phase
    ); """
make_symbol(ldlib, "SigGenFrequencyToPhase", "ps6000SigGenFrequencyToPhase", c_uint32,
            [c_int16, c_double, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps6000SigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
make_symbol(ldlib, "SigGenArbitraryMinMaxValues", "ps6000SigGenArbitraryMinMaxValues", c_uint32,
            [c_int16, c_void_p, c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps6000SigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
make_symbol(ldlib, "SigGenSoftwareControl", "ps6000SigGenSoftwareControl", c_uint32, [c_int16, c_int16])

""" PICO_STATUS ps6000SetSimpleTrigger
    (
        int16_t                     handle,
        int16_t                     enable,
        PS6000_CHANNEL              source,
        int16_t                     threshold,
        PS6000_THRESHOLD_DIRECTION  direction,
        uint32_t                    delay,
        int16_t                     autoTrigger_ms
    ); """
make_symbol(ldlib, "SetSimpleTrigger", "ps6000SetSimpleTrigger", c_uint32,
            [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16])

""" PICO_STATUS ps6000SetEts
    (
        int16_t          handle,
        PS6000_ETS_MODE  mode,
        int16_t          etsCycles,
        int16_t          etsInterleave,
        int32_t         *sampleTimePicoseconds
    ); """
make_symbol(ldlib, "SetEts", "ps6000SetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p])

""" PICO_STATUS ps6000SetTriggerChannelProperties
    (
        int16_t                            handle,
        PS6000_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                            nChannelProperties,
        int16_t                            auxOutputEnable,
        int32_t                            autoTriggerMilliseconds
    ); """
make_symbol(ldlib, "SetTriggerChannelProperties", "ps6000SetTriggerChannelProperties", c_uint32,
            [c_int16, c_void_p, c_int16, c_int16, c_int32])

""" PICO_STATUS ps6000SetTriggerChannelConditions
    (
        int16_t                    handle,
        PS6000_TRIGGER_CONDITIONS *conditions,
        int16_t                    nConditions
    ); """
make_symbol(ldlib, "SetTriggerChannelConditions", "ps6000SetTriggerChannelConditions", c_uint32,
            [c_int16, c_void_p, c_int16])

""" PICO_STATUS ps6000SetTriggerChannelDirections
    (
        int16_t                       handle,
        PS6000_THRESHOLD_DIRECTION  channelA,
        PS6000_THRESHOLD_DIRECTION  channelB,
        PS6000_THRESHOLD_DIRECTION  channelC,
        PS6000_THRESHOLD_DIRECTION  channelD,
        PS6000_THRESHOLD_DIRECTION  ext,
        PS6000_THRESHOLD_DIRECTION  aux
    ); """
make_symbol(ldlib, "SetTriggerChannelDirections", "ps6000SetTriggerChannelDirections", c_uint32,
            [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32])

""" PICO_STATUS ps6000SetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
make_symbol(ldlib, "SetTriggerDelay", "ps6000SetTriggerDelay", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps6000SetPulseWidthQualifier
    (
        int16_t                     handle,
        PS6000_PWQ_CONDITIONS      *conditions,
        int16_t                     nConditions,
        PS6000_THRESHOLD_DIRECTION  direction,
        uint32_t                    lower,
        uint32_t                    upper,
        PS6000_PULSE_WIDTH_TYPE     type
    ); """
make_symbol(ldlib, "SetPulseWidthQualifier", "ps6000SetPulseWidthQualifier", c_uint32,
            [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps6000IsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
make_symbol(ldlib, "IsTriggerOrPulseWidthQualifierEnabled", "ps6000IsTriggerOrPulseWidthQualifierEnabled", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps6000GetTriggerTimeOffset
    (
        int16_t            handle,
        uint32_t          *timeUpper,
        uint32_t          *timeLower,
        PS6000_TIME_UNITS *timeUnits,
        uint32_t           segmentIndex
    ); """

""" PICO_STATUS ps6000GetTriggerTimeOffset64
    (
        int16_t              handle,
        int64_t           *time,
        PS6000_TIME_UNITS *timeUnits,
        uint32_t      segmentIndex
    ); """
make_symbol(ldlib, "GetTriggerTimeOffset", "ps6000GetTriggerTimeOffset64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32])

""" PICO_STATUS ps6000GetValuesTriggerTimeOffsetBulk
    (
        int16_t            handle,
        uint32_t          *timesUpper,
        uint32_t          *timesLower,
        PS6000_TIME_UNITS *timeUnits,
        uint32_t           fromSegmentIndex,
        uint32_t           toSegmentIndex
    ); """

""" PICO_STATUS ps6000GetValuesTriggerTimeOffsetBulk64
    (
        int16_t            handle,
        int64_t           *times,
        PS6000_TIME_UNITS *timeUnits,
        uint32_t           fromSegmentIndex,
        uint32_t           toSegmentIndex
    ); """
make_symbol(ldlib, "GetValuesTriggerTimeOffsetBulk", "ps6000GetValuesTriggerTimeOffsetBulk64", c_uint32,
            [c_int16, c_void_p, c_void_p, c_uint32, c_uint32])

""" PICO_STATUS ps6000SetDataBuffers
    (
        int16_t            handle,
        PS6000_CHANNEL     channel,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        uint32_t           bufferLth,
        PS6000_RATIO_MODE  downSampleRatioMode
    ); """
make_symbol(ldlib, "SetDataBuffers", "ps6000SetDataBuffers", c_uint32,
            [c_int16, c_int32, c_void_p, c_void_p, c_uint32, c_int32])

""" PICO_STATUS ps6000SetDataBuffer
    (
        int16_t            handle,
        PS6000_CHANNEL     channel,
        int16_t           *buffer,
        uint32_t           bufferLth,
        PS6000_RATIO_MODE  downSampleRatioMode
    ); """
make_symbol(ldlib, "SetDataBuffer", "ps6000SetDataBuffer", c_uint32, [c_int16, c_int32, c_void_p, c_uint32, c_int32])

""" PICO_STATUS PREF2 PREF3 (ps6000SetDataBufferBulk)
    (
        int16_t            handle,
        PS6000_CHANNEL     channel,
        int16_t           *buffer,
        uint32_t           bufferLth,
        uint32_t           waveform,
        PS6000_RATIO_MODE  downSampleRatioMode
    ); """
make_symbol(ldlib, "SetDataBufferBulk", "ps6000SetDataBufferBulk", c_uint32,
            [c_int16, c_int32, c_void_p, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps6000SetDataBuffersBulk
    (
        int16_t            handle,
        PS6000_CHANNEL     channel,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        uint32_t           bufferLth,
        uint32_t           waveform,
        PS6000_RATIO_MODE  downSampleRatioMode
    ); """
make_symbol(ldlib, "SetDataBuffersBulk", "ps6000SetDataBuffersBulk", c_uint32,
            [c_int16, c_int32, c_void_p, c_void_p, c_uint32, c_uint32, c_int32])

""" PICO_STATUS ps6000SetEtsTimeBuffer
    (
        int16_t   handle,
        int64_t  *buffer,
        uint32_t  bufferLth
    ); """
make_symbol(ldlib, "SetEtsTimeBuffer", "ps6000SetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_uint32])

""" PICO_STATUS ps6000SetEtsTimeBuffers
    (
        int16_t   handle,
        uint32_t *timeUpper,
        uint32_t *timeLower,
        uint32_t  bufferLth
    ); """

""" PICO_STATUS ps6000RunBlock
    (
        int16_t           handle,
        uint32_t          noOfPreTriggerSamples,
        uint32_t          noOfPostTriggerSamples,
        uint32_t          timebase,
        int16_t           oversample,
        int32_t          *timeIndisposedMs,
        uint32_t          segmentIndex,
        ps6000BlockReady  lpReady,
        void             *pParameter
    ); """
make_symbol(ldlib, "RunBlock", "ps6000RunBlock", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_int16, c_void_p, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps6000IsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
make_symbol(ldlib, "IsReady", "ps6000IsReady", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps6000RunStreaming
    (
        int16_t            handle,
        uint32_t          *sampleInterval,
        PS6000_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t           maxPreTriggerSamples,
        uint32_t           maxPostPreTriggerSamples,
        int16_t            autoStop,
        uint32_t           downSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        uint32_t           overviewBufferSize
    ); """
make_symbol(ldlib, "RunStreaming", "ps6000RunStreaming", c_uint32,
            [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32])

""" PICO_STATUS ps6000GetStreamingLatestValues
    (
        int16_t               handle,
        ps6000StreamingReady  lpPs6000Ready,
        void                 *pParameter
    ); """
make_symbol(ldlib, "GetStreamingLatestValues", "ps6000GetStreamingLatestValues", c_uint32,
            [c_int16, c_void_p, c_void_p])

""" PICO_STATUS ps6000NoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
make_symbol(ldlib, "NoOfStreamingValues", "ps6000NoOfStreamingValues", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps6000GetMaxDownSampleRatio
    (
        int16_t            handle,
        uint32_t           noOfUnaggreatedSamples,
        uint32_t          *maxDownSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        uint32_t           segmentIndex
    ); """
make_symbol(ldlib, "GetMaxDownSampleRatio", "ps6000GetMaxDownSampleRatio", c_uint32,
            [c_int16, c_uint32, c_void_p, c_int32, c_uint32])

""" PICO_STATUS ps6000GetValues
    (
        int16_t            handle,
        uint32_t           startIndex,
        uint32_t          *noOfSamples,
        uint32_t           downSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        uint32_t           segmentIndex,
        int16_t           *overflow
    ); """
make_symbol(ldlib, "GetValues", "ps6000GetValues", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps6000GetValuesBulk
    (
        int16_t            handle,
        uint32_t          *noOfSamples,
        uint32_t           fromSegmentIndex,
        uint32_t           toSegmentIndex,
        uint32_t           downSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        int16_t           *overflow
    ); """
make_symbol(ldlib, "GetValuesBulk", "ps6000GetValuesBulk", c_uint32,
            [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p])

""" PICO_STATUS ps6000GetValuesAsync
    (
        int16_t            handle,
        uint32_t           startIndex,
        uint32_t           noOfSamples,
        uint32_t           downSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        uint32_t           segmentIndex,
        void              *lpDataReady,
        void              *pParameter
    ); """
make_symbol(ldlib, "GetValuesAsync", "ps6000GetValuesAsync", c_uint32,
            [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p])

""" PICO_STATUS ps6000GetValuesOverlapped
    (
        int16_t            handle,
        uint32_t           startIndex,
        uint32_t          *noOfSamples,
        uint32_t           downSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        uint32_t           segmentIndex,
        int16_t           *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlapped", "ps6000GetValuesOverlapped", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p])

""" PICO_STATUS ps6000GetValuesOverlappedBulk
    (
        int16_t            handle,
        uint32_t           startIndex,
        uint32_t          *noOfSamples,
        uint32_t           downSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        uint32_t           fromSegmentIndex,
        uint32_t           toSegmentIndex,
        int16_t           *overflow
    ); """
make_symbol(ldlib, "GetValuesOverlappedBulk", "ps6000GetValuesOverlappedBulk", c_uint32,
            [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p])

""" PICO_STATUS ps6000GetValuesBulkAsyc
    (
        int16_t            handle,
        uint32_t           startIndex,
        uint32_t          *noOfSamples,
        uint32_t           downSampleRatio,
        PS6000_RATIO_MODE  downSampleRatioMode,
        uint32_t           fromSegmentIndex,
        uint32_t           toSegmentIndex,
        int16_t           *overflow
    ); """

""" PICO_STATUS ps6000GetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
make_symbol(ldlib, "GetNoOfCaptures", "ps6000GetNoOfCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps6000GetNoOfProcessedCaptures
    (
        int16_t   handle,
        uint32_t *nProcessedCaptures
    ); """
make_symbol(ldlib, "GetNoOfProcessedCaptures", "ps6000GetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p])

""" PICO_STATUS ps6000Stop
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "Stop", "ps6000Stop", c_uint32, [c_int16, ])

""" PICO_STATUS ps6000SetNoOfCaptures
    (
        int16_t   handle,
        uint32_t  nCaptures
    ); """
make_symbol(ldlib, "SetNoOfCaptures", "ps6000SetNoOfCaptures", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps6000SetWaveformLimiter
    (
        int16_t   handle,
        uint32_t  nWaveformsPerSecond
    ); """
make_symbol(ldlib, "SetWaveformLimiter", "ps6000SetWaveformLimiter", c_uint32, [c_int16, c_uint32])

""" PICO_STATUS ps6000EnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
make_symbol(ldlib, "EnumerateUnits", "ps6000EnumerateUnits", c_uint32, [c_void_p, c_void_p, c_void_p])

""" PICO_STATUS ps6000SetExternalClock
    (
        int16_t                    handle,
        PS6000_EXTERNAL_FREQUENCY  frequency,
        int16_t                    threshold
    ); """
make_symbol(ldlib, "SetExternalClock", "ps6000SetExternalClock", c_uint32, [c_int16, c_int32, c_int16])

""" PICO_STATUS ps6000PingUnit
    (
        int16_t  handle
    ); """
make_symbol(ldlib, "PingUnit", "ps6000PingUnit", c_uint32, [c_int16, ])

""" PICO_STATUS ps6000GetAnalogueOffset
    (
        int16_t          handle,
        PS6000_RANGE     range,
        PS6000_COUPLING  coupling,
        float           *maximumVoltage,
        float           *minimumVoltage
    ); """
make_symbol(ldlib, "GetAnalogueOffset", "ps6000GetAnalogueOffset", c_uint32,
            [c_int16, c_int32, c_int32, c_void_p, c_void_p])


class ChannelState(ps5000base.ChannelState):
    """ Object describing state of the channel """

    def __init__(self):
        super(ChannelState, self).__init__()
        self.bwlimit = BWLimit.bw_full


class Couplings(ps5000base.Couplings):
    """ Coupling selection """
    ac = 0
    dc1M = 1
    dc50 = 2
    dc = dc1M
    labels = {ac: "AC", dc1M: "DC 1M\234", dc50: "DC 50\234"}


class RatioModes(ps5000base.RatioModes):
    """ Collection of Downsample modes """
    raw = 0
    none = raw
    agg = 1
    aggregate = agg
    avg = 2
    average = avg
    dec = 4
    decimate = dec
    map = (raw, agg, avg, dec)
    labels = {raw: "raw", agg: "agg", avg: "avg", dec: "dec"}

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


class BWLimit(dict2class):
    bw_full = 0
    bw_20M = 1
    bw_25M = 2
    map = (bw_full, bw_20M, bw_25M)
    labels = {bw_full: "full", bw_20M: "20MHz", bw_25M: "25MHz"}

variants = ("6402", "6402A", "6402B", "6402C", "6402D", "6403", "6403A", "6403B", "6403C", "6403D",
            "6404", "6404A", "6404B", "6404C", "6404D", "6407", "6408", )


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
        self.info.num_channels = 4
        self.info.has_siggen = True
        self.info.siggen_frequency = 20000000
        self.info.siggen_min = 0
        self.info.siggen_max = 4000000
        self.info.min_range = self.m.Ranges.r50mv
        self.info.max_range = self.m.Ranges.r20v
        if self.info.variant_info == "6402":
            self.info.max_segments = 31250
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "6402A":
            self.info.max_segments = 125000
            self.info.has_awg = False
        elif self.info.variant_info == "6402B":
            self.info.max_segments = 250000
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "6402C":
            self.info.max_segments = 250000
            self.info.has_awg = False
        elif self.info.variant_info == "6402D":
            self.info.max_segments = 500000
            self.info.has_awg = True
            self.info.awg_size = 65536
        elif self.info.variant_info == "6403":
            self.info.max_segments = 1000000
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "6403A":
            self.info.max_segments = 250000
            self.info.has_awg = False
        elif self.info.variant_info == "6403B":
            self.info.max_segments = 500000
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "6403C":
            self.info.max_segments = 500000
            self.info.has_awg = False
        elif self.info.variant_info == "6403D":
            self.info.max_segments = 1000000
            self.info.has_awg = True
            self.info.awg_size = 65536
        elif self.info.variant_info == "6404":
            self.info.max_segments = 1000000
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "6404A":
            self.info.max_segments = 500000
            self.info.has_awg = False
        elif self.info.variant_info == "6404B":
            self.info.max_segments = 1000000
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "6404C":
            self.info.max_segments = 1000000
            self.info.has_awg = False
        elif self.info.variant_info == "6404D":
            self.info.max_segments = 2000000
            self.info.has_awg = True
            self.info.awg_size = 65536
        elif self.info.variant_info == "6407":
            self.info.max_segments = 1000000
            self.info.has_awg = True
            self.info.awg_size = 16384
        elif self.info.variant_info == "6408":
            self.info.max_segments = 32768
            self.info.has_awg = True
            self.info.awg_size = 16384
        else:
            return pico_num("PICO_INFO_UNAVAILABLE")
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
        mem = c_uint32()
        status = self._memory_segments(self._segments, byref(mem))
        self.info.memory = mem.value
        self.info.memps = mem.value
        return status

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
        mem = c_uint32()
        status = self._memory_segments(segments, byref(mem))
        if status == pico_num("PICO_OK"):
            self._segments = segments
            self.info.memps = mem.value
            return status, mem.value
        return status, 0

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
            state.coupling = self.m.Couplings.dc1M
            state.range = Ranges.r500mv
            state.offset = 0
            state.bwlimit = BWLimit.bw_full

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
        return pico_num("PICO_NOT_USED")

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
                                  c_int32(state.range), c_float(state.offset), c_int32(state.bwlimit))
        if status == pico_num("PICO_OK"):
            state.overvoltaged = False
            self._channel_set[channel] = deepcopy(state)
        return status

    def _set_data_buffers(self, line, buffer_max, buffer_min, bufflen, segment, mode):
        return ldlib.SetDataBuffers(self._chandle, c_int32(line), buffer_max, buffer_min,
                                    c_uint32(bufflen), c_int32(mode))

    def _setbuffers(self, indexes, enable=True):
        if self._start_segment is not None and self._stop_segment is not None:
            segments = (self._start_segment,) if self._start_segment == self._stop_segment \
                else range(self._start_segment, self._stop_segment + 1) if self._stop_segment > self._start_segment \
                else range(self._start_segment, self._segments) + range(0, self._stop_segment + 1)

            for index in indexes:
                buff = self._buffers[index]
                with buff.access_lock:
                    number = segments.index(buff.segment) if segments is not None else 0
                    status = ldlib.SetDataBuffersBulk(self._chandle, c_int32(buff.channel),
                                                      buff.data.ctypes if enable else None,
                                                      (buff.data_min.ctypes
                                                       if enable and buff.mode == self.m.RatioModes.agg else None),
                                                      c_uint32(buff.samples), c_uint32(number), c_int32(buff.mode))
                if status != pico_num("PICO_OK"):
                    return status
        else:
            for index in indexes:
                buff = self._buffers[index]
                with buff.access_lock:
                    status = \
                        ldlib.SetDataBuffers(self._chandle, c_int32(buff.channel),
                                             buff.data.ctypes if enable else None,
                                             (buff.data_min.ctypes
                                              if enable and buff.mode == self.m.RatioModes.agg else None),
                                             c_uint32(buff.samples), c_int32(buff.mode))
                if status != pico_num("PICO_OK"):
                    return status
        return pico_num("PICO_OK")

    def _get_timebase(self, timebase, samples, ref_interval, oversample, ref_maxsamples, segment):
        return ldlib.GetTimebase(self._chandle, c_uint32(timebase), c_uint32(samples), ref_interval,
                                 c_int16(oversample), ref_maxsamples, c_uint32(segment))

    def _run_block(self, pretrig, posttrig, timebase, oversample, ref_time, segment, ref_cb, ref_cb_param):
        return ldlib.RunBlock(self._chandle, c_uint32(pretrig), c_uint32(posttrig), c_uint32(timebase),
                              c_int16(oversample), ref_time, c_uint32(segment), ref_cb, ref_cb_param)

    @staticmethod
    def _streaming_ready():
        if sys.platform == "win32":
            return WINFUNCTYPE(None, c_int16, c_uint32, c_uint32, c_int16, c_uint32, c_int16, c_int16, c_void_p)
        else:
            return CFUNCTYPE(None, c_int16, c_uint32, c_uint32, c_int16, c_uint32, c_int16, c_int16, c_void_p)


def enumerate_units():
    global ldlib
    return ps5000base.enumerate_units(ldlib)
