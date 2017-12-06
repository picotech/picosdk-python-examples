#!/usr/bin/python
"""
 *     Filename: block_capture.py
 *     
 *	   Description:
 *			Example script showing a block mode data capture from 
 *			a PicoScope oscilloscope using the driver API functions 
 * 			from the drivers listed below.
 * 	   
 *	  @author: mario
 * 
 *    Copyright (C) 2014 - 2017 Pico Technology Ltd. See LICENSE file for terms.
 *
"""

from optparse import OptionParser, OptionGroup
import importlib
from exceptions import ImportError, OSError
import matplotlib.pyplot as plt
from example_utils import *
import os
from time import strftime

modules = ("ps2000", "ps2000a", "ps3000", "ps3000a", "ps4000", "ps4000a", "ps5000a", "ps6000")

TESTED = PASSED = FAILED = IGNORED = 0


def _options():
    global modules
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-g", "--graph",
                      action="store_true", dest="graph", default=False,
                      help="Generate graph. default: %default")
    parser.add_option("-G", "--show-graph",
                      action="store_true", dest="show_graph", default=False,
                      help="Display the graph (implies -g). default: %default")
    parser.add_option("-X", "--check",
                      action="store_true", dest="validate", default=False,
                      help="Validate results against perfect sine.\t"
                           "default: %default")
    parser.add_option("-l", "--std-limit",
                      action="store", type="float", dest="std_limit",
                      metavar="LIMIT", default=3.0,
                      help="Standard error limit in % of the results.\t"
                           "default: %default%")
    parser.add_option("-L", "--max-limit",
                      action="store", type="float", dest="max_limit",
                      metavar="LIMIT", default=10.0,
                      help="Maximum error limit in % of the results.\t"
                           "default: %default%")
    parser.add_option("-O", "--output",
                      action="store", type="string", dest="output",
                      metavar="DIR", default="",
                      help="Where to write test results.\t\t"
                           "default: None")
    parser.add_option("-A", "--autoname",
                      action="store_true", dest="autoname", default=False,
                      help="Automatically create subfolder for test results.\t"
                           "Format: YYYYMMDD-hhmmss-variant-serial")
    parser.add_option("-P", "--print-options",
                      action="store_true", dest="print_options", default=False,
                      help="Print command line options in the output.\t\t"
                           "default: %default")

    group = OptionGroup(parser, "Device Options")
    group.add_option("-d", "--drivers",
                     action="store", type="string", dest="drivers",
                     metavar="DRIVERS", default=",".join(modules),
                     help="Comma separated list of drivers.\t\t"
                          "default: All supported")
    group.add_option("-v", "--variant",
                     action="store", type="string", dest="variant",
                     metavar="VARIANT", default="",
                     help="String defining variant to open.\t\t"
                          "default: None (open any)")
    group.add_option("-b", "--serial", "--batch",
                     action="store", type="string", dest="serial",
                     metavar="SERIAL", default="",
                     help="String to open ps by serial.\t\t\t"
                          "default: None (match any)")
    group.add_option("-w", "--warnings",
                     action="store_true", dest="warnings",
                     default=False,
                     help="Raise power supply and usb port warnings as errors.\t"
                          "default: %default")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Channels Options")
    group.add_option("-c", "--channels",
                     action="store", type="string", dest="channels",
                     metavar="CHANNELS", default="",
                     help="Comma separated list of channels to test.\t"
                          "default: all available")
    group.add_option("-r", "--range",
                     action="store", type="int", dest="range",
                     metavar="RANGE", default=7,
                     help="Channels range, default: +/-2V(7)")
    parser.add_option_group(group)

    group = OptionGroup(parser, "SigGen Options")
    group.add_option("-f", "--frequency",
                     action="store", type="float", dest="frequency",
                     metavar="FREQ", default=1000.0,
                     help="Siggen frequency to test.\t\t\t"
                          "default: %default")
    group.add_option("-a", "--amplitude",
                     action="store", type="int", dest="pk2pk",
                     metavar="PK2PK", default=3000000,
                     help="Siggen amplitude to set in microvolts.\t\t"
                          "default: %default")
    group.add_option("-o", "--offset",
                     action="store", type="int", dest="offset",
                     metavar="OFFSET", default=0,
                     help="Siggen offset to apply, in microvolts.\t\t"
                          "default: %default")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Trigger Options")
    group.add_option("-T", "--trigger",
                     action="store_true", dest="trigger",
                     default=False,
                     help="Use trigger, default: %default")
    group.add_option("-C", "--triggc",
                     action="store", type="int", dest="triggc",
                     metavar="ENUM", default=-1,
                     help="Channel on trigger; set -1 to pick first available.")
    group.add_option("-V", "--triggv",
                     action="store", type=float, dest="triggv",
                     metavar="VRATIO", default=0.0,
                     help="Vertical trigger ratio:\t\t\t\t\t"
                          "threshold as (-1.0, 1.0) of current range.\t"
                          "default: %default")
    group.add_option("-H", "--triggh",
                     action="store", type=float, dest="triggh",
                     metavar="HRATIO", default=0.5,
                     help="Horizontal trigger ratio (0.0, 1.0)\t\t"
                          "default: %default")
    group.add_option("-D", "--triggd",
                     action="store", type="int", dest="triggd",
                     metavar="DIR", default=2,
                     help="Trigger direction; 2: rising, 3: falling\t"
                          "default: 2: rising")
    group.add_option("-W", "--triggw",
                     action="store", type="int", dest="triggw",
                     metavar="BLOCKS", default=3,
                     help="Trigger wait how many (samples * interval) blocks to wait for trigger. "
                          "default: %default")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Sampling Options")
    group.add_option("-s", "--samples",
                     action="store", type="int", dest="max_samples",
                     metavar="COUNT", default=10000,
                     help="Maximum number of raw samples per channel.\t\t"
                          "Limited to device capabilities where necessary.\t"
                          "default: %default")
    group.add_option("-m", "--modes",
                     action="store", type="string", dest="modes",
                     metavar="MODES", default="raw",
                     help="Reduction mode to run, use raw \t\t\t\t"
                          "or comma separated list from avg, agg, dec\t"
                          "default: %default")
    group.add_option("-R", "--ratios",
                     action="store", type="string", dest="ratios",
                     metavar="RATIOS", default="1",
                     help="Reduction ratios as comma separated list,\t\t"
                          "ignored for RAW mode. default: %default")
    group.add_option("-S", "--max-segments",
                     action="store", type="int", dest="segments",
                     metavar="SEGMENTS", default=1,
                     help="Number of segments to set.\t\t\t"
                          "default: %default")
    group.add_option("-B", "--segment",
                     action="store", type="string", dest="segment",
                     metavar="SEGMENT|START-STOP", default="0",
                     help="Segment number to collect from (0, max-segments-1).\t"
                          "Specify as range for bulk collection: start-stop.\t\t"
                          "default: %default")
    group.add_option("-i", "--interval",
                     action="store", type="float", dest="interval",
                     metavar="NS", default=0.0,
                     help="Desired sample interval in nanoseconds.\t\t\t"
                          "Set to 0 for count selection.")
    group.add_option("-t", "--cycles",
                     action="store", type="int", dest="cycles",
                     metavar="CYCLES", default=3,
                     help="Calculate interval from number of cycles\t\t\t"
                          "of the waveform of siggen frequency to test.\t\t"
                          "Ignored if explicit interval given. default: %default")
    group.add_option("-M", "--overlapped",
                     action="store_true", dest="overlapped",
                     default=False,
                     help="Use overlapped buffers. default: %default")
    group.add_option("-Y", "--ets-mode",
                     action="store", type="string", dest="ets_mode",
                     metavar="MODE", default="off",
                     help="Set ETS mode for collection: off, fast, slow.\t\t"
                          "default: %default")
    group.add_option("-y", "--ets-cycles",
                     action="store", type="int", dest="ets_cycles",
                     metavar="CYCLES", default=100,
                     help="ETS cycles, default: %default")
    group.add_option("-u", "--ets-interleaves",
                     action="store", type="int", dest="ets_interleaves",
                     metavar="INTERLEAVES", default=10,
                     help="ETS interleaves, default: %default")
    parser.add_option_group(group)

    return parser


def validate_sine(ps, index, std_limit=3.0, max_limit=10.0):
    global TESTED, PASSED, FAILED, IGNORED
    status, info = ps.get_buffer_info(index)
    name = "Ch%s S%d M%s R%d" % (ps.m.Channels.labels[info["channel"]], info["segment"],
                                 ps.m.RatioModes.labels[info["mode"]], info["downsample"])
    if info["mode"] == ps.m.RatioModes.agg:
        status, data_min, data_max = ps.get_min_max_data(index)
        data = data_min / 2 + data_max / 2
    else:
        status, data = ps.get_buffer_data(index)
    error_check("Buffer %d data" % index, status)
    # Butterworth low pass
    # Filter order
    o = 2
    # Cutoff frequency
    fc = min(1.0, (1000.0 / info["samples"]))
    # construct the filter
    numerator, denominator = signal.butter(o, fc, output='ba')
    # apply the filter
    smooth = signal.filtfilt(numerator, denominator, data)
    sig_min = smooth.min()
    sig_max = smooth.max()
    a = (float(abs(sig_min)) + float(abs(sig_max))) / 2.0
    b = (sig_min + sig_max) / 2.0
    zero_crossings = np.where(np.diff(np.signbit(smooth - b)))[0]
    ticks = ()
    r = min(zero_crossings[0] / 2 if len(zero_crossings) > 0 else 1, int(info["samples"] / 250))
    last_z = 0
    for z in zero_crossings:
        if z != 0 and z == last_z + 1:
            last_z = z
            continue
        last_z = z
        try:
            if smooth[z - r] < smooth[z + r + 1]:
                d = float(smooth[z + 1]) - float(smooth[z])
                if d != 0.0:
                    ticks += (z - (smooth[z] - b) / d, )
                else:
                    ticks += (z, )
        except IndexError:
            pass
    if len(ticks) < 2:
        p_warn("%s insufficient zero crossings to validate the signal." % name)
        TESTED += 1
        IGNORED += 1
        return smooth, smooth
    elif len(ticks) > 50:
        p_warn("%s great number of zero crossings found: %d, accuracy compromised"
               % (name, len(ticks)))
    last = None
    ticksum = 0
    for t in ticks:
        if last is not None:
            ticksum += t - last
        last = t
    period = float(ticksum) / (len(ticks) - 1)
    f = 1000000000.0 / (period * info["real_interval"])
    p_info("%s frequency %.2fHz" % (name, f / info["downsample"]))
    s = 2 * pi / ((1.0 / f) / (info["real_interval"] / 1000000000.0))
    ideal = np.array([a * sin((float(x) - ticks[0]) * s) + b for x in range(0, info["samples"])])
    diff = data - ideal
    std_error = np.std(diff) / ps.info.max_adc * 200
    max_error = np.max(np.abs(diff)) / ps.info.max_adc * 200
    if p_assert(title="%s std" % name, value=std_error, limit=std_limit):
        PASSED += 1
    else:
        FAILED += 1
    if p_assert(title="%s max" % name, value=max_error, limit=max_limit):
        PASSED += 1
    else:
        FAILED += 1
    TESTED += 2
    return ideal, smooth


def main():
    global modules
    parser = _options()
    (options, args) = parser.parse_args()
    p_info("Block mode test started %s" % strftime("%Y-%m-%d %H:%M:%S"))

    if options.print_options:
        p_info("Main Options")
        for opt in parser.option_list:
            option = opt.get_opt_string()
            if option != "--help":
                value = getattr(options, opt.dest)
                p_info("%s: %s%s" % (opt, value, " *" if opt.default != value else ""))
        for grp in parser.option_groups:
            p_info(grp.title)
            for opt in grp.option_list:
                value = getattr(options, opt.dest)
                p_info("%s: %s%s" % (opt, value, " *" if opt.default != value else ""))

    # test output directory
    if options.output != "":
        outdir = os.path.abspath(options.output)
        if len(outdir) <= 1:
            p_error("Invalid output directory specified.")
        if not (os.path.exists(outdir) and os.path.isdir(outdir)):
            p_error("Output directory not found.")
    else:
        outdir = None

    # test ps opening selection
    if options.drivers != ",".join(modules):
        if "," not in options.drivers:
            drivers = (options.drivers, )
        else:
            drivers = tuple(options.drivers.split(","))
        for d in drivers:
            if d not in modules:
                p_error("Unknown driver %s specified." % d)
            else:
                break
        else:
            p_error("Device driver not recognised.")
    else:
        drivers = modules

    module = None

    if options.variant != "":
        for d in drivers:
            try:
                module = importlib.import_module("picosdk.%s" % d)
                if options.variant not in module.variants:
                    module = None
                    continue
                else:
                    p_info("Variant %s found supported in %s module." % (options.variant, module.name))
                    break
            except ImportError as ex:
                p_warn("module %s: %s" % (d, ex.message))
                module = None
        if module is None:
            p_error("variant %s not supported." % options.variant)
    else:
        module = None

    if options.serial != "":
        if module is not None:
            units = module.enumerate_units()
            if len(units) == 0 or options.serial not in units:
                p_error("Device with serial %s not found via %s driver." % (options.serial, module.name))
        else:
            for d in drivers:
                try:
                    module = importlib.import_module("picosdk.%s" % d)
                    units = module.enumerate_units()
                    if len(units) > 0 and options.serial in units:
                        break
                except ImportError as ex:
                    p_warn("module %s: %s" % (d, ex.message))
                    module = None

    if module is None:
        units = ()
        for d in drivers:
            try:
                module = importlib.import_module("picosdk.%s" % d)
                units = module.enumerate_units()
                if len(units) > 0:
                    break
            except ImportError as ex:
                    p_warn("module %s: %s" % (d, ex.message))
                    module = None
        if len(units) == 0:
            p_error("Device not found.")

    if module is None:
        p_error("Internal error, no driver available.")

    ps = module.Device()
    status = ps.open_unit(serial=(options.serial if options.serial != "" else None))
    if status == st.pico_num("DEVICE_NOT_FOUND"):
        p_error("Device not found.")
    else:
        if status in (st.pico_num("PICO_USB3_0_DEVICE_NON_USB3_0_PORT"),
                      st.pico_num("PICO_POWER_SUPPLY_NOT_CONNECTED")):
            if options.warnings:
                if status == st.pico_num("PICO_USB3_0_DEVICE_NON_USB3_0_PORT"):
                    p_error("Device not on USB3.0 port.")
                else:
                    p_error("Power supply required.")
            else:
                if status == st.pico_num("PICO_USB3_0_DEVICE_NON_USB3_0_PORT"):
                    p_warn("Device not on USB3.0 port.")
                else:
                    p_warn("Power supply required.")
                status = ps.set_power_source(power=st.pico_num("PICO_POWER_SUPPLY_NOT_CONNECTED"))
                if status != st.pico_num("PICO_OK"):
                    p_error("Power setup failed with %s" % st.pico_tag(status))
                else:
                    status = ps.load_info()

    if status != st.pico_num("PICO_OK"):
        p_error("Device open failed with %s" % (st.pico_tag(status)))

    # initialize the log
    if outdir is not None:
        if options.autoname:
            dname = ("%s_%s_%s" %
                     (strftime("%Y%m%d_%H%M%S"), ps.info.variant_info, ps.info.batch_and_serial)).replace("/", "_")
            logdir = os.path.join(outdir, dname)
        else:
            logdir = outdir
        try:
            if not os.path.exists(logdir):
                os.mkdir(logdir)
            logfile = os.path.join(logdir, "block_test.log")
        except OSError:
            logfile = None
            p_warn("Failed to create output directory")
    else:
        logfile = None
        logdir = None

    if logfile is not None:
        try:
            logd = open(logfile, "a")
            p_setlogd(logd)
        except OSError:
            logd = None
            pass
    else:
        logd = None

    p_info("Device connected: %s %s" % (ps.info.variant_info, ps.info.batch_and_serial))
    p_info("Driver: %s" % ps.info.driver_version)
    p_info("Firmware: %s/%s" % (ps.info.firmware_version_1, ps.info.firmware_version_2))

    test_finished = False
    global TESTED, PASSED, FAILED, IGNORED
    try:
        dev_channels = ps.m.Channels.map[:ps.info.num_channels]
        if options.channels != "":
            channels = ()

            if "," not in options.channels:
                channels_in = (options.channels, )
            else:
                channels_in = options.channels.split(",")
            for c in channels_in:
                if len(c) > 1 and c not in "0123456789":
                    p_error("Wrong channel specified: %s" % c)
                else:
                    c = int(c)
                    if c not in dev_channels:
                        p_error("Channel %d not supported by device." % c)
                    if c not in channels:
                        channels += (c,)
            if len(channels) == 0:
                p_error("No suitable channel parsed")
            channels = sorted(channels)
        else:
            channels = dev_channels

        if options.range not in ps.info.channel_ranges.keys():
            p_error("Range %d not supported by the device." % options.range)

        for c in dev_channels:
            status, state = ps.get_channel_state(channel=c)
            state.range = options.range
            state.enabled = c in channels
            error_check("Channel %s Setup" % ps.m.Channels.labels[c], ps.set_channel(channel=c, state=state))

        if options.ets_mode not in ("off", "fast", "slow"):
            p_error("ETS mode %s not supported" % options.ets_mode)
        if options.ets_mode == "off":
            ets = False
        else:
            ets = True
            try:
                ets_mode = getattr(ps.m.ETSModes, options.ets_mode)
            except (IndexError, ValueError):
                p_error("ETS mode %s not support by the device" % options.ets_mode)
            error_check("ETS Setup", ps.ets_setup(mode=ets_mode, cycles=options.ets_cycles,
                                                  interleaves=options.ets_interleaves))
            p_info("Using ETS %s mode with %d cycles and %d interleaves"
                   % (options.ets_mode, options.ets_cycles, options.ets_interleaves))
        if not ps.info.has_siggen:
            p_warn("Device is missing Signal Generator.")
            p_warn("Make sure to provide alternative source of signal to selected channels.")
        else:
            if options.frequency <= 0 or options.frequency > ps.info.siggen_frequency:
                p_error("Siggen frequency %fHz out of range (0,%f)" % (options.frequency, ps.info.siggen_frequency))
            if options.pk2pk < ps.info.siggen_min or options.pk2pk > ps.info.siggen_max:
                p_error("Siggen amplitude %duV out of range (%d, %d)"
                        % (options.pk2pk, ps.info.siggen_min, ps.info.siggen_max))
            if options.offset > ps.info.siggen_max - ps.info.siggen_min:
                p_error("Siggen offset %duV out of range (0, %d)"
                        % (options.offset, ps.info.siggen_max - ps.info.siggen_min))
            error_check("Siggen setup", ps.set_simple_sig_gen(wave_type=ps.m.WaveTypes.sine,
                                                              frequency=options.frequency,
                                                              pk2pk=options.pk2pk, offset=options.offset))
        if ets and not options.trigger:
            p_warn("ETS mode implies use of a trigger, enabling")
            options.trigger = True

        if options.trigger:
            if options.triggc == -1:
                triggc = channels[0]
            else:
                if options.triggc not in channels:
                    p_error("Trigger channel incorrect")
                else:
                    triggc = options.triggc
            if options.triggd not in ps.m.ThresholdDirections.simple:
                p_error("Trigger direction not supported")

        if "-" in options.segment:
            try:
                start_segment = int(options.segment.split("-")[0])
                stop_segment = int(options.segment.split("-")[1])
            except (ValueError, IndexError):
                p_error("Invalid segment range specification")
            if start_segment == stop_segment:
                segment = start_segment
                bulk = False
            else:
                bulk = True
        else:
            try:
                segment = int(options.segment)
            except ValueError:
                p_error("Invalid segment specification")
            bulk = False

        if options.segments <= 0:
            p_error("Wrong number of segments: %d" % options.segments)
        if options.segments > ps.info.max_segments:
            p_error("Too many segments %d > %d" % (options.segments, ps.info.max_segments))
        segments = options.segments
        if bulk:
            if not (0 <= start_segment < segments and 0 <= stop_segment < segments):
                p_error("Segments range out of limits %d-%d (0, %d)" % (start_segment, stop_segment, segments))
        else:
            if not 0 <= segment < segments:
                p_error("Segment out of range %d (0, %d)" % (segment, segments))
        status, max_samples = ps.set_memory_segments(segments)
        error_check("Segments setup", status)
        if bulk:
            p_info("Rapid collection of segments from %d to %d" % (start_segment, stop_segment))
            if start_segment > stop_segment:
                p_info("Collection will wrap at %d segment" % (segments - 1))
        else:
            p_info("Collecting segment %d/%d%s" % (segment, options.segments,
                                                   " overlapped" if options.overlapped else ""))
        cnum = len(channels)
        if cnum in (1, 2):
            div = cnum
        elif cnum in (3, 4):
            div = 4
        elif cnum >= 5:
            div = 8
        else:
            p_error("Unsupported number of channels.")
        if max_samples < div * options.max_samples:
            bufflen = int(max_samples / div)
            p_warn("Number of raw samples per channel reduced to %d" % bufflen)
        else:
            bufflen = options.max_samples
        p_info("Raw samples length: %d" % bufflen)

        if "," not in options.modes:
            in_modes = (options.modes, )
        else:
            in_modes = options.modes.split(",")

        if "raw" in in_modes:
            if len(in_modes) > 1:
                p_warn("Modes selection reduced to raw")
            modes = ("raw", )
            ratios = (1,)
        else:
            modes = ()
            for m in in_modes:
                if m not in modes:
                    if m not in ps.m.RatioModes.labels.values():
                        p_error("Unsupported reduction mode; %s" % m)
                    else:
                        modes += (m, )
            if len(modes) == 0:
                p_error("Reduction mode not selected.")
            elif ets:
                p_error("ETS mode not supported with data reduction")
            if "," not in options.ratios:
                in_ratios = (options.ratios, )
            else:
                in_ratios = options.ratios.split(",")
            ratios = ()
            for r0 in in_ratios:
                r = int(r0)
                if r not in ratios:
                    if r <= 1:
                        p_warn("Discarding invalid ratio %s" % r0)
                    elif r > bufflen:
                        p_warn("Ratio over the limit %s > %d" % (r0, bufflen))
                    else:
                        ratios += (r, )
            if len(ratios) == 0:
                p_error("Reduction ratio not available.")

        if not ets:
            if options.interval != 0:
                if options.interval < 0:
                    p_error("Invalid interval %.2f" % options.interval)
                interval = options.interval
                p_info("Raw sample interval specified as %.2fns" % interval)
            else:
                if options.cycles < 1:
                    p_error("Invalid number of waveform cycles %d < 1" % options.cycles)
                interval = (options.cycles * 1.0 / options.frequency / bufflen) * 1000000000
                p_info("Raw sample interval calculated as %.2fns" % interval)
        else:
            interval = 1

        if options.trigger:
            if ets:
                triggw = 0
            else:
                if options.triggw < 0:
                    p_error("Invalid trigger wait count: %d < 0" % options.triggw)
                elif options.triggw != 0:
                    triggw = max(1, int(options.triggw * bufflen * interval / 1000000.0))
                    p_info("Trigger wait calculated as %dms" % triggw)
            error_check("VTrigger setup", ps.set_simple_trigger(enabled=True, source=triggc, threshold=options.triggv,
                                                                direction=options.triggd, delay=0, waitfor=triggw))
            error_check("HTrigger setup", ps.set_horizontal_trigger_ratio(ratio=options.triggh))
        else:
            error_check("Trigger setup", ps.set_simple_trigger(enabled=False, source=0, threshold=0,
                                                               direction=0, delay=0, waitfor=0))
        mode = 0
        num_modes = ()
        for m in ps.m.RatioModes.labels.keys():
            if ps.m.RatioModes.labels[m] in modes:
                mode |= m
                num_modes += (m, )
        if bulk:
            segments_list = range(start_segment, segments) + range(0, stop_segment + 1) \
                if start_segment > stop_segment \
                else range(start_segment, stop_segment + 1)
        else:
            segments_list = (segment, )
        for r in ratios:
            p_info("Testing downsample ratio %d" % r)
            samples = int(bufflen / r)
            buffers = dict()
            for s in segments_list:
                buffers[s] = dict()
                for m in num_modes:
                    buffers[s][m] = dict()
                    for c in channels:
                        status, buffers[s][m][c] = ps.locate_buffer(channel=c, samples=samples,
                                                                    segment=s, mode=m, downsample=r)
                        error_check("Buffer chan %s mode %s ratio %d on segment %d setup"
                                    % (ps.m.Channels.labels[c], ps.m.RatioModes.labels[m], r, s), status)
            if bulk:
                error_check("Collection start", ps.collect_segments(start_segment=start_segment,
                                                                    stop_segment=stop_segment, interval=interval))
            else:
                error_check("Collection start", ps.collect_segment(segment=segment, interval=interval,
                                                                   overlapped=options.overlapped))
            if ets:
                status, picos = ps.get_ets_status()
                error_check("ETS run", status)
                p_info("ETS ran at %dps" % picos)
            data = dict()
            if options.validate:
                ideal = dict()
                smooth = dict()
            info = None
            for s in segments_list:
                data[s] = dict()
                if options.validate:
                    ideal[s] = dict()
                    smooth[s] = dict()
                for c in channels:
                    data[s][c] = dict()
                    if options.validate:
                        ideal[s][c] = dict()
                        smooth[s][c] = dict()
                    for m in num_modes:
                        if info is None:
                            status, info = ps.get_buffer_info(buffers[s][m][c])
                            p_info("Effective interval of the trace %.2fns" % info["real_interval"])
                        if m == ps.m.RatioModes.agg:
                            status, data[s][c]["min"], data[s][c]["max"] = ps.get_min_max_data(buffers[s][m][c])
                        else:
                            status, data[s][c][ps.m.RatioModes.labels[m]] = ps.get_buffer_data(buffers[s][m][c])
                        error_check("Buffer chan %s mode %s ratio %d data"
                                    % (ps.m.Channels.labels[c], ps.m.RatioModes.labels[m], r), status)
                        if options.validate:
                            ideal[s][c][ps.m.RatioModes.labels[m]], smooth[s][c][ps.m.RatioModes.labels[m]] = \
                                validate_sine(ps, buffers[s][m][c], options.std_limit, options.max_limit)

            if options.graph or options.show_graph:
                fig, pts = plt.subplots(len(channels), len(modes) * len(segments_list), sharex=True, sharey=bulk)
                fig.canvas.set_window_title("Ratio %d" % r)

                timecut = r * info["real_interval"] * info["samples"]
                time_units = ps.m.TimeUnits.ns
                while timecut > 1000:
                    timecut /= 1000.0
                    time_units += 1
                time_step = timecut / info["samples"]
                if ets:
                    s, time_domain, d = ps.get_ets_data(info["index"])
                    graph_limit = [time_domain.min(), time_domain.max()]
                else:
                    graph_limit = [0, time_step * (info["samples"] - 1)]
                    time_domain = time_step * np.arange(0, info["samples"])

            for i in range(0, len(channels)):
                c = channels[i]
                for j in range(0, len(segments_list)):
                    s = segments_list[j]
                    for k in range(0, len(num_modes)):
                        m = num_modes[k]
                        if options.graph or options.show_graph:
                            if len(num_modes) * len(segments_list) > 1:
                                if len(channels) > 1:
                                    p = pts[i][k * len(segments_list) + j]
                                else:
                                    p = pts[k * len(segments_list) + j]
                            else:
                                if len(channels) * len(segments_list) > 1:
                                    p = pts[i * len(segments_list) + j]
                                else:
                                    p = pts
                            p.clear()
                            p.set_xlim(graph_limit)

                            if m == ps.m.RatioModes.agg:
                                data_limit = min(len(data[s][c]["max"]), info["samples"])
                                li, = p.plot(time_domain[:data_limit], data[s][c]["max"][:data_limit])
                                li.set_color(colors[i])
                                li, = p.plot(time_domain[:data_limit], data[s][c]["min"][:data_limit])
                                li.set_color(ncolors[c])
                            else:
                                data_limit = min(len(data[s][c][ps.m.RatioModes.labels[m]]), info["samples"])
                                li, = p.plot(time_domain[:data_limit],
                                             data[s][c][ps.m.RatioModes.labels[m]][:data_limit])
                                li.set_color(colors[c])
                            if options.validate:
                                li, = p.plot(time_domain[:data_limit],
                                             ideal[s][c][ps.m.RatioModes.labels[m]][:data_limit], '--')
                                li.set_color(idealcolor)

                            p.set_xlabel("Ch%s%s M%s R%d [%s]"
                                         % (ps.m.Channels.labels[c],
                                            (" S%d" % s) if len(segments_list) > 1 else "",
                                            ps.m.RatioModes.labels[m], r,
                                            ps.m.TimeUnits.ascii_labels[time_units]))
                        if options.trigger and triggc == c:
                            triggx = options.triggh * samples
                            triggy = options.triggv * ps.info.max_adc
                            if options.graph or options.show_graph:
                                marker = '^' if options.triggd == ps.m.ThresholdDirections.rising else \
                                    ('v' if options.triggd == ps.m.ThresholdDirections.falling else 'D')
                                if ets:
                                    li, = p.plot(0, [triggy], marker, ms=9)
                                else:
                                    li, = p.plot([triggx * time_step], [triggy], marker, ms=9)
                                li.set_color(triggcolor)
                            if options.validate:
                                x1 = max(0, triggx - 3)
                                x = max(0, triggx - 1)
                                if m == ps.m.RatioModes.agg:
                                    x2 = min(triggx + 3, len(data[s][c]["max"]) - 1)
                                    y1 = (float(data[s][c]["min"][x1]) + float(data[s][c]["max"][x1])) / 2.0
                                    y2 = (float(data[s][c]["min"][x2]) + float(data[s][c]["max"][x2])) / 2.0
                                    y = (float(data[s][c]["min"][x]) + float(data[s][c]["max"][x])) / 2.0
                                else:
                                    x2 = min(triggx + 3, len(data[s][c][ps.m.RatioModes.labels[m]]) - 1)
                                    y1 = data[s][c][ps.m.RatioModes.labels[m]][x1]
                                    y2 = data[s][c][ps.m.RatioModes.labels[m]][x2]
                                    y = data[s][c][ps.m.RatioModes.labels[m]][x]
                                if options.triggd == ps.m.ThresholdDirections.rising:
                                    found = y1 <= y <= y2
                                elif options.triggd == ps.m.ThresholdDirections.falling:
                                    found = y2 <= y <= y1
                                else:
                                    found = y1 <= y <= y2 or y2 <= y <= y1
                                title = "Ch%s S%d M%s R%d trigger %s H:%.2f/V:%.2f X:%d/Y:%d %s" \
                                        % (ps.m.Channels.labels[c], s, ps.m.RatioModes.labels[m], r,
                                           ps.m.ThresholdDirections.labels[options.triggd],
                                           options.triggh, options.triggv, x, int(y),
                                           "found" if found else "not found")
                                if p_assert(title=title, result=found):
                                    PASSED += 1
                                else:
                                    FAILED += 1
                                TESTED += 1
                        if options.graph or options.show_graph:
                            p.grid()
            if (options.graph or options.show_graph) and logdir is not None:
                saveas = "block_c%s_m_%s_r%d_s%d_t%s.png" % (
                    "".join([str(c) for c in channels]), "_".join(modes),
                    r, bufflen,
                    "off" if not options.trigger else ("on_V%.2f_H%.2f" % (options.triggv, options.triggh))
                )
                saveas = os.path.join(logdir, saveas)
                p_info("Saving graphs as %s" % saveas)
                try:
                    fig.savefig(saveas, dpi=300)
                except OSError:
                    p_warn("Failed to write %s" % saveas)
        if options.show_graph:
            plt.show(block=True)
        test_finished = True
    finally:
        if not test_finished:
            p_error("Test run failed", end=False)
        p_info("Test results pass/fail/ignored/total: %d/%d/%d/%d" % (PASSED, FAILED, IGNORED, TESTED))
        if logd is not None:
            try:
                logd.close()
            except OSError:
                pass
        ps.close_unit()

if __name__ == "__main__":
    main()
