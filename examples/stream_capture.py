#!/usr/bin/python
"""
 *     Filename: stream_capture.py
 *     
 *	   Description:
 *			Example script showing streaming mode data capture from 
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
                      help="Output dir for test results.\t\t\t"
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
                     help="Trigger wait how many (total_samples * interval) blocks to wait for trigger. "
                          "default: %default")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Sampling Options")
    group.add_option("-s", "--samples",
                     action="store", type="int", dest="samples",
                     metavar="COUNT", default=10000,
                     help="Number of overview buffer samples.\t\t"
                          "default: %default")
    group.add_option("-e", "--total-samples",
                     action="store", type="int", dest="max_samples",
                     metavar="COUNT", default=100000,
                     help="Final number of samples to collect.\t\t"
                          "default: %default")
    group.add_option("-E", "--auto-stop",
                     action="store_true", dest="autostop", default=False,
                     help="Set device to autostop streaming when total number of samples is reached. "
                          "default: stop during data playback.")
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
    group.add_option("-i", "--interval",
                     action="store", type="float", dest="interval",
                     metavar="NS", default=0.0,
                     help="Desired sample interval in nanoseconds.\t\t\t"
                          "Set to 0 for count selection.")
    group.add_option("-u", "--units",
                     action="store", type="int", dest="units",
                     metavar="ENUM", default=2,
                     help="Interval units enum.\t\t\t\t"
                          "default: %default")
    group.add_option("-t", "--cycles",
                     action="store", type="int", dest="cycles",
                     metavar="CYCLES", default=3,
                     help="Calculate interval from number of cycles\t\t\t"
                          "of the waveform of siggen frequency to test.\t\t"
                          "Ignored if explicit interval given. default: %default")
    group.add_option("-F", "--tape-filename",
                     action="store", type="string", dest="tape_file",
                     metavar="FILE", default="",
                     help="Streaming tape file location - absolute or relative to output dir. "
                          "default: tmp memory file")
    group.add_option("-N", "--chapter-prefix",
                     action="store", type="string", dest="chapter",
                     metavar="PREFIX", default="stream",
                     help="Streaming chapter prefix. default: %default")
    parser.add_option_group(group)

    return parser


def main():
    global modules
    global TESTED, PASSED, FAILED, IGNORED
    parser = _options()
    (options, args) = parser.parse_args()

    p_info("Streaming mode test started %s" % strftime("%Y-%m-%d %H:%M:%S"))

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
            logfile = os.path.join(logdir, "stream_test.log")
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

    tape_file = None
    if options.tape_file != "":
        try:
            if outdir is not None and not os.path.isabs(options.tape_file):
                tape_file = os.path.join(outdir, options.tape_file)
            else:
                tape_file = os.path.normpath(options.tape_file)
            if not os.path.exists(os.path.dirname(tape_file)):
                p_error("Tape file destination directory doesn't exist.")
        except OSError:
            p_warn("Failed to parse tape file option.")

    p_info("Device connected: %s %s" % (ps.info.variant_info, ps.info.batch_and_serial))
    p_info("Driver: %s" % ps.info.driver_version)
    p_info("Firmware: %s/%s" % (ps.info.firmware_version_1, ps.info.firmware_version_2))

    test_finished = False
    try:
        tape = ps.m.StreamingTape(filename=tape_file, stats=True)
        error_check("Tape load", ps.load_tape(tape))

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

        if "," not in options.modes:
            in_modes = (options.modes, )
        else:
            in_modes = options.modes.split(",")

        if "raw" in in_modes:
            if len(in_modes) > 1:
                p_warn("Modes selection reduced to raw")
            modes = ("raw", )
            ratios = (1, )
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
                    else:
                        ratios += (r, )
            if len(ratios) == 0:
                p_error("Reduction ratio not available.")
        if options.samples > options.max_samples:
            bufflen = options.max_samples
            p_warn("Limited overview buffer size to %d samples" % options.max_samples)
        else:
            bufflen = options.samples
        if options.interval != 0:
            if options.interval < 0:
                p_error("Invalid interval %d" % options.interval)
            interval = int(options.interval)
            if options.units not in ps.m.TimeUnits.map:
                p_error("Invalid interval time units %d" % options.units)
            nano_interval = interval * float(pow(10, ps.m.TimeUnits.nanofactors(options.units)))
            p_info("Raw sample interval specified as %d%s" % (interval, ps.m.TimeUnits.ascii_labels[options.units]))
        else:
            if options.cycles < 1:
                p_error("Invalid number of waveform cycles %d < 1" % options.cycles)
            interval = int(options.cycles * 1.0 / options.frequency / options.max_samples * 1000000000)
            p_info("Raw sample interval calculated as %dns" % interval)
            nano_interval = interval
        if options.trigger:
            if options.triggw < 0:
                p_error("Invalid trigger wait count: %d < 0" % options.triggw)
            triggw = int(options.triggw * options.max_samples * nano_interval / 1000000.0)
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

        for r in ratios:
            p_info("Testing downsample ratio %d" % r)
            buffers = dict()
            for c in channels:
                buffers[c] = dict()
                for m in num_modes:
                    buffers[c][m] = dict()
                    if m == ps.m.RatioModes.agg:
                        buffers[c]["min"] = np.empty(shape=(options.max_samples, ), dtype=ps.m.ctypes.c_int16)
                        buffers[c]["max"] = np.empty(shape=(options.max_samples, ), dtype=ps.m.ctypes.c_int16)
                    else:
                        buffers[c][ps.m.RatioModes.labels[m]] =\
                            np.empty(shape=(options.max_samples, ), dtype=ps.m.ctypes.c_int16)

            chapter = ("%s_r%d" % (options.chapter, r))
            error_check("Streaming start",
                        ps.start_recording(interval=interval, units=options.units, mode=mode, downsample=r,
                                           memlength=bufflen, chapter=chapter,
                                           limit=(options.max_samples if options.autostop else 0)))
            wait4data = max(10.0, 2.0 * bufflen * r * nano_interval / 1000000000.0)
            if not tape.wait2start(chapter=chapter, timeout=wait4data):
                p_error("Streaming has not started within reasonable timescale")

            go_on = True
            total_samples = 0
            triggered = -1
            while go_on:
                record = tape.play_next(chapter=chapter, wait=True, timeout=wait4data)
                if record is not None and hasattr(record, "buffers"):
                    if options.autostop and hasattr(record, "final") and record.final:
                        go_on = False
                    top_to = total_samples + record.samples
                    for c in channels:
                        for m in num_modes:
                            l = ps.m.RatioModes.labels[m]
                            if top_to <= options.max_samples:
                                if m == ps.m.RatioModes.agg:
                                    buffers[c]["min"][total_samples:top_to] =\
                                        record.buffers[c]["min"][record.start:record.samples]
                                    buffers[c]["max"][total_samples:top_to] =\
                                        record.buffers[c]["max"][record.start:record.samples]
                                else:
                                    buffers[c][l][total_samples:top_to] =\
                                        record.buffers[c][l][record.start:record.samples]
                            else:
                                if m == ps.m.RatioModes.agg:
                                    buffers[c]["min"] = np.append(buffers[c]["min"][:total_samples],
                                                                  record.buffers[c]["min"][record.start:record.samples])
                                    buffers[c]["max"] = np.append(buffers[c]["max"][:total_samples],
                                                                  record.buffers[c]["max"][record.start:record.samples])
                                else:
                                    buffers[c][l] = np.append(buffers[c][l][:total_samples],
                                                              record.buffers[c][l][record.start:record.samples])
                    if options.trigger and record.triggerSet:
                        if record.triggered:
                            triggered = total_samples + record.triggerAt
                            if go_on and top_to >= triggered + options.max_samples * (1 - (options.triggh % 1)):
                                go_on = False
                                ps.stop_recording()
                        elif go_on and triggered >= 0 \
                                and top_to >= triggered + options.max_samples * (1 - (options.triggh % 1)):
                            go_on = False
                            ps.stop_recording()
                    elif go_on and top_to >= options.max_samples:
                                go_on = False
                                ps.stop_recording()
                    total_samples += record.samples
                else:
                    go_on = False
                    p_error("Streaming playback interrupted")
            tape.wait2finish()
            if tape_file is not None:
                stats = tape.pull_stats()
                if stats is not None and isinstance(stats, dict):
                    sum_d = 0
                    sum_t = 0.0
                    for s in stats.keys():
                        sum_d += stats[s]["data_len"]
                        sum_t += stats[s]["time"]

                    data_units = ["", "k", "M", "G", "T"]
                    data_total = 2.0 * sum_d

                    data_unit = 0
                    while data_total > 1000:
                        data_total /= 1024.0
                        data_unit += 1
                        if data_unit == 4:
                            break
                    p_info("Total data writen to the storage: %.2f%sB" % (data_total, data_units[data_unit]))
                    if sum_t > 0:
                        data_avg = 2.0 * sum_d / sum_t
                    else:
                        data_avg = 0
                    data_unit = 0
                    while data_avg > 1000:
                        data_avg /= 1024.0
                        data_unit += 1
                        if data_unit == 4:
                            break
                    p_info("Average data storage write speed: %.2f%sB/s" % (data_avg, data_units[data_unit]))
                else:
                    p_warn("Failed to receive data storage statistics")
            if options.validate:
                ideal = dict()
                smooth = dict()
                for c in channels:
                    ideal[c] = dict()
                    smooth[c] = dict()
                    for m in num_modes:
                        name = "Ch%s M%s R%d" % (ps.m.Channels.labels[c], ps.m.RatioModes.labels[m], r)
                        if m == ps.m.RatioModes.agg:
                            data = buffers[c]["min"] / 2 + buffers[c]["max"] / 2
                        else:
                            data = buffers[c][ps.m.RatioModes.labels[m]]
                        # Butterworth low pass
                        # Filter order
                        o = 2
                        # Cutoff frequency
                        fc = min(1.0, (1000.0 / len(data)))
                        # construct the filter
                        numerator, denominator = signal.butter(o, fc, output='ba')
                        # apply the filter
                        smooth[c][m] = signal.filtfilt(numerator, denominator, data)
                        ideal[c][m] = smooth[c][m]
                        sig_min = smooth[c][m].min()
                        sig_max = smooth[c][m].max()
                        a = (float(abs(sig_min)) + float(abs(sig_max))) / 2.0
                        b = (sig_min + sig_max) / 2.0
                        zero_crossings = np.where(np.diff(np.signbit(smooth[c][m] - b)))[0]
                        ticks = ()
                        rnd = min(zero_crossings[0] / 2 if len(zero_crossings) > 0 else 1, int(len(data) / 250))
                        last_z = 0
                        for z in zero_crossings:
                            if z != 0 and z == last_z + 1:
                                last_z = z
                                continue
                            last_z = z
                            try:
                                if smooth[c][m][z - rnd] < smooth[c][m][z + rnd + 1]:
                                    d = float(smooth[c][m][z + 1]) - float(smooth[c][m][z])
                                    if d != 0.0:
                                        ticks += (z - (smooth[c][m][z] - b) / d, )
                                    else:
                                        ticks += (z, )
                            except IndexError:
                                pass
                        if len(ticks) < 2:
                            p_warn("%s insufficient zero crossings to validate the signal." % name)
                            IGNORED += 1
                            TESTED += 1
                            continue
                        elif len(ticks) > 50:
                            p_warn("%s great number of zero crossings found: %d, accuracy compromised"
                                   % (name, len(ticks)))
                        last = None
                        ticksum = 0
                        for t in ticks:
                            if last is not None:
                                ticksum += t - last
                            last = t
                        f = 1000000000.0 / (float(ticksum) / (len(ticks) - 1) * float(nano_interval))
                        p_info("%s frequency %.2fHz" % (name, f / r))
                        s = 2 * pi / ((1.0 / f) / (float(nano_interval) / 1000000000.0))
                        ideal[c][m] = np.array([a * sin((float(x) - ticks[0]) * s) + b for x in range(0, len(data))])
                        diff = data - ideal[c][m]
                        std_error = np.std(diff) / ps.info.max_adc * 200
                        max_error = np.max(np.abs(diff)) / ps.info.max_adc * 200
                        if p_assert(title="%s std" % name, value=std_error, limit=options.std_limit):
                            PASSED += 1
                        else:
                            FAILED += 1

                        if p_assert(title="%s max" % name, value=max_error, limit=options.max_limit):
                            PASSED += 1
                        else:
                            FAILED += 1
                        TESTED += 2
            if options.graph or options.show_graph:
                fig, pts = plt.subplots(len(channels), len(modes), sharex=True)
                fig.canvas.set_window_title("Ratio %d" % r)

            for i in range(0, len(channels)):
                c = channels[i]
                for j in range(0, len(num_modes)):
                    m = num_modes[j]
                    name = "Ch%s M%s R%d" % (ps.m.Channels.labels[c], ps.m.RatioModes.labels[m], r)
                    if options.graph or options.show_graph:
                        if len(num_modes) > 1:
                            if len(channels) > 1:
                                p = pts[i][j]
                            else:
                                p = pts[j]
                        else:
                            if len(channels) > 1:
                                p = pts[i]
                            else:
                                p = pts
                        p.clear()

                        if m == ps.m.RatioModes.agg:
                            data_range = len(buffers[c]["max"])
                        else:
                            data_range = len(buffers[c][ps.m.RatioModes.labels[m]])
                        total_time = r * float(nano_interval) * data_range
                        time_units = ps.m.TimeUnits.ns
                        while total_time > 1000:
                            total_time /= 1000.0
                            time_units += 1
                            if time_units >= ps.m.TimeUnits.s:
                                break
                        time_step = total_time / data_range
                        graph_limit = time_step * (data_range - 1)
                        time_domain = time_step * np.arange(0, data_range, dtype=float)
                        p.set_xlim([0, graph_limit])
                        if m == ps.m.RatioModes.agg:
                            li, = p.plot(time_domain, buffers[c]["max"])
                            li.set_color(colors[i])
                            li, = p.plot(time_domain, buffers[c]["min"])
                            li.set_color(ncolors[c])
                        else:
                            li, = p.plot(time_domain, buffers[c][ps.m.RatioModes.labels[m]])
                            li.set_color(colors[c])
                        if options.validate:
                            li, = p.plot(time_domain, ideal[c][m], '--')
                            li.set_color(idealcolor)
                            # li, = p.plot(time_domain, smooth[c][m], '.')
                            # li.set_color(colors[c])

                        p.set_xlabel("%s [%s]" % (name, ps.m.TimeUnits.ascii_labels[time_units]))
                    if options.trigger and triggc == c:
                        triggx = triggered
                        triggy = options.triggv * ps.info.max_adc
                        if options.validate:
                            x1 = triggx - 2
                            x2 = triggx + 2
                            x = triggx
                            if m == ps.m.RatioModes.agg:
                                y1 = (float(buffers[c]["min"][x1]) + float(buffers[c]["max"][x1])) / 2.0
                                y2 = (float(buffers[c]["min"][x2]) + float(buffers[c]["max"][x2])) / 2.0
                                y = (float(buffers[c]["min"][x]) + float(buffers[c]["max"][x])) / 2.0
                            else:
                                y1 = buffers[c][ps.m.RatioModes.labels[m]][x1]
                                y2 = buffers[c][ps.m.RatioModes.labels[m]][x2]
                                y = buffers[c][ps.m.RatioModes.labels[m]][x]
                            if options.triggd == ps.m.ThresholdDirections.rising:
                                found = y1 < y < y2
                            elif options.triggd == ps.m.ThresholdDirections.falling:
                                found = y2 < y < y1
                            else:
                                found = y1 < y < y2 or y2 < y < y1
                            title = "%s trigger %s H:%.2f/V:%.2f X:%d/Y:%d %s" \
                                    % (name, ps.m.ThresholdDirections.labels[options.triggd],
                                       options.triggh, options.triggv, x, int(y),
                                       "found" if found else "not found")
                            if p_assert(title=title, result=found):
                                PASSED += 1
                            else:
                                FAILED += 1
                            TESTED += 1
                        if options.graph or options.show_graph:
                            marker = '^' if options.triggd == ps.m.ThresholdDirections.rising else \
                                ('v' if options.triggd == ps.m.ThresholdDirections.falling else 'D')
                            li, = p.plot([triggx * time_step], [triggy], marker, ms=9)
                            li.set_color(triggcolor)
                    if options.graph or options.show_graph:
                        p.grid()

            if (options.graph or options.show_graph) and logdir is not None:
                saveas = "stream_c%s_m_%s_r%d_s%d_t%s.png" % (
                    "".join([str(c) for c in channels]), "_".join(modes),
                    r, options.max_samples,
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
        if tape is not None:
            tape.wait2finish()
            tape.close()
        ps.stop()
        ps.close_unit()

if __name__ == "__main__":
    main()
