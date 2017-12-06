#
# Copyright (C) 2014-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Basic and helper functions/classes used in PicoScope modules
"""

import ctypes
from ctypes import *
from ctypes.util import find_library
import tables as tb
import numpy as np
import threading as th
import Queue
import sys
import os.path
from time import time, strftime, sleep
import warnings
import multiprocessing
from exceptions import AttributeError, OSError, TypeError
from copy import deepcopy
from picosdk.picostatus import pico_num

""" disable warnings from PyTables """
for cat in ("UndoRedoWarning", "NaturalNameWarning", "PerformanceWarning", "FlavorWarning", "FiltersWarning",
            "OldIndexWarning", "DataTypeWarning", "Incompat16Warning", "ExperimentalFeatureWarning"):
    try:
        warnings.filterwarnings('ignore', category=getattr(tb, cat))
    except AttributeError:
        pass


def psloadlib(name):
    """ Loads driver library
    :param name: driver name
    :type name: str
    :returns: ctypes reference to the library
    :rtype: object
    """
    result = None
    try:
        if sys.platform == 'win32':
            result = ctypes.WinDLL(find_library(name))
        else:
            result = cdll.LoadLibrary(find_library(name))
    except OSError as ex:
        print name, "import(%d): Library not found" % sys.exc_info()[-1].tb_lineno
    return result


def make_symbol(ldlib, name, symbol, restype, argtypes):
    """ Helper for library symbols generation
    :param ldlib: loaded library reference
    :param name: function call to use
    :param symbol: library symbol to attach function to
    :param restype: library symbol return type
    :param argtypes: list of library symbol parameters
    :return: None
    """
    try:
        ldlib[name] = ldlib.lib[symbol]
        ldlib[name].restype = restype
        ldlib[name].argtypes = argtypes
    except AttributeError:
        print ldlib.name, name, "import(%d): Symbol not found" % sys.exc_info()[-1].tb_lineno
    except TypeError:
        pass
    except Exception as ex:
        print name, "import(%d):" % sys.exc_info()[-1].tb_lineno, ex, type(ex)


class dict2class(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self, ident=0):
        s = "{\n"
        for k in sorted(self.__dict__.keys()):
            s += ("    " * (ident + 1)) + str(k) + ": "
            if isinstance(self.__dict__[k], type(self)):
                s += self.__dict__[k].__repr__((ident + 2))
                s += ",\n" + ("    " * (ident + 1))
            else:
                s += repr(self.__dict__[k])
                s += ",\n"
        s += ("    " * (ident if ident > 0 else 0))
        s += "}"
        return s

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def __contains__(self, item):
        return item in self.__dict__

    def add(self, key, value):
        self.__dict__[key] = value

    def __iter__(self):
        return iter(self.__dict__)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v


class StreamingTape(object):
    """ Streaming data storage class """
    recfmt = "record%08d"
    filters = tb.Filters(complib='blosc', complevel=9)
    atom = tb.Atom.from_dtype(np.dtype("int16"))

    def __init__(self, filename=None, title=None, limit=1000, overwrite=True, stats=False):
        self._filename = filename
        self._title = title
        self._limit = limit
        self._overwrite = overwrite
        self._stats = stats
        self.lastError = None
        self._recordLock = th.Lock()
        self._readLock = th.Lock()
        for l in (self._recordLock, self._readLock):
            if l.acquire(False):
                l.release()
        self._closing = False
        self._start_processor()
        self._setup_processor()

    def _start_processor(self):
        self._recordControl = multiprocessing.Queue()
        self._recordRead = multiprocessing.Queue()
        self._recordWrite = multiprocessing.Queue()
        self._recordWatchIn = multiprocessing.Queue()
        self._recordWatchOut = multiprocessing.Queue()
        self._recordProcess = RecordsProcessor(self._recordControl,
                                               self._recordRead,
                                               self._recordWrite,
                                               self._recordWatchIn,
                                               self._recordWatchOut)
        self._recordProcess.start()
        self._watchdogEvent = th.Event()
        if self._watchdogEvent.is_set():
            self._watchdogEvent.clear()
        self._watchdogThread = th.Thread(target=self._watchdog_worker, args=(None, ))
        self._watchdogThread.start()
        self._isProcessing = True

    def _watchdog_worker(self, args):
        keepalive = None
        try:
            self._recordWatchOut.put(True)
        except Exception as ex:
            print "Watchdog Init(%d):" % sys.exc_info()[-1].tb_lineno, ex, type(ex)
        with self._readLock:
            self._recordControl.put({"Command": "Watchdog", "args": None})
        while not self._watchdogEvent.wait(0.1):
            try:
                keepalive = self._recordWatchIn.get(True, 1.0)
            except Queue.Empty:
                keepalive = None
            if keepalive is not None:
                try:
                    self._recordWatchOut.put(True)
                except Exception as ex:
                    print "Watchdog Send(%d):" % sys.exc_info()[-1].tb_lineno, ex, type(ex)
            else:
                self._watchdogEvent.set()
                self._isProcessing = False

    def _setup_processor(self):
        if self._recordProcess.is_alive():
            with self._readLock:
                self._recordControl.put({"Command": "Open",
                                         "args": {"filename": self._filename,
                                                  "title": self._title,
                                                  "limit": self._limit,
                                                  "overwrite": self._overwrite,
                                                  "stats": self._stats}},
                                        True)
                response = None
                try:
                    response = self._recordRead.get(True, timeout=7.0)
                except Queue.Empty:
                    response = None
                if isinstance(response, basestring) and response == "OK":
                    return pico_num("PICO_OK")
                return pico_num("PICO_FILE_WRITE_FAILED")
        else:
            return pico_num("PICO_OPERATION_FAILED")

    def is_processing(self):
        return self._isProcessing

    def eject(self):
        self._close()

    def close(self):
        self._close()

    def unload(self):
        self._close()

    def _close(self):
        self._closing = True
        if self._recordProcess is not None and self._recordProcess.is_alive():
            with self._readLock:
                self._recordControl.put({"Command": "Exit", "args": None}, True)
                self._recordRead.get()
            self._recordProcess.join()
        self._recordProcess = None
        if not self._watchdogEvent.is_set():
            self._watchdogEvent.set()
        self._watchdogThread.join()

        self._recordControl._buffer.clear()
        self._recordControl.close()
        self._recordControl.join_thread()

        self._recordRead._buffer.clear()
        self._recordRead.close()
        self._recordRead.join_thread()

        self._recordWrite._buffer.clear()
        self._recordWrite.close()
        self._recordWrite.join_thread()

    def record(self, records):
        if self._closing or self._recordProcess is None or not self._recordProcess.is_alive():
            return pico_num("PICO_CANCELLED")
        status = pico_num("PICO_OK")
        try:
            with self._recordLock:
                if records is not None:
                    self._recordWrite.put(records.side_copy())
                else:
                    self._recordWrite.put(None)
        except Exception as ex:
            self.lastError = ex.message
            print "Tape Record(%d):" % sys.exc_info()[-1].tb_lineno, self.lastError, type(ex)
            status = pico_num("PICO_CANCELLED")
        return status

    def wait2finish(self, timeout=10.0):
        timeout += time()
        if self._recordProcess is not None and self._recordProcess.is_alive():
            while not self._closing and self._recordWrite.qsize() > 0 and (timeout == 0 or time() < timeout):
                sleep(0.01)

    def wait2start(self, chapter=None, timeout=10.0):
        timeout += time()
        while not self._closing and (timeout == 0 or time() < timeout):
            chapters = self.chapters()
            if len(chapters) > 0:
                if chapter is None or chapter in chapters:
                    return True
            sleep(0.01)
        return False

    def chapters(self):
        with self._readLock:
            self._recordControl.put({"Command": "Chapters", "args": None})
            chapters = None
            try:
                chapters = self._recordRead.get(True)
            except Queue.Empty:
                chapters = None
        if chapters is None:
            return []
        else:
            chapters.sort()
            return chapters

    def play_next(self, chapter=None, wait=True, timeout=10.0, purge=False):
        with self._readLock:
            self._recordControl.put({"Command": "Next", "args": {"chapter": chapter, "wait": wait, "purge": purge}})
            nrec = None
            try:
                nrec = self._recordRead.get(True, timeout)
            except Queue.Empty:
                nrec = None
            if nrec is None:
                return nrec
            if isinstance(nrec, basestring):
                if wait and nrec == "WAIT":
                    try:
                        nrec = self._recordRead.get(True, timeout)
                    except Queue.Empty:
                        nrec = None
                else:
                    return None
            return nrec

    def play_last(self):
        with self._readLock:
            self._recordControl.put({"Command": "Last", "args": None})
            try:
                last = self._recordRead.get(True)
            except Queue.Empty:
                last = None
        return last

    def pull_stats(self):
        if not self._stats:
            return None
        with self._readLock:
            self._recordControl.put({"Command": "Stats", "args": None})
            try:
                stats = self._recordRead.get(True)
            except Queue.Empty:
                stats = None
        return stats

    def erase(self):
        pass


class StreamingTapeRecording(dict2class):

    def __init__(self):
        self.samples = 0
        self.start = 0
        self.bufflen = 0
        self.buffers = {}

    def side_copy(self):
        try:
            clone = StreamingTapeRecording()
            for key in self.keys():
                if not isinstance(self[key], dict):
                    clone[key] = self[key]
                else:
                    clone[key] = {}
                    for row in self[key].keys():
                        if not isinstance(self[key][row], dict):
                            clone[key][row] = self[key][row]
                        else:
                            clone[key][row] = {}
                            for data in self[key][row].keys():
                                if not isinstance(self[key][row][data], np.ndarray):
                                    clone[key][row][data] = self[key][row][data]
                                else:
                                    clone[key][row][data] = np.empty(shape=(self.bufflen,), dtype=c_int16)
                                    clone[key][row][data][:self.samples] = \
                                        self[key][row][data][self.start:(self.start + self.samples)]
            clone.start = 0
        except Exception as ex:
            print "Tape Side Copy(%d):" % sys.exc_info()[-1].tb_lineno, ex.message
            clone = None
        return clone

    def top_up(self, rec):
        try:
            if not isinstance(rec, StreamingTapeRecording) or self.samples > self.bufflen:
                return None
            if self.samples == self.bufflen:
                return rec
            if self.start != 0:
                for c in self.buffers.keys():
                    for key in self.buffers[c].keys():
                        if isinstance(self.buffers[c][key], np.ndarray):
                            a = np.empty(shape=(self.bufflen, ), dtype=c_int16)
                            a[:self.samples] = self.buffers[c][key][self.start:(self.start + self.samples)]
                            self.buffers[c][key] = a
                self.start = 0
            if self.samples + rec.samples > self.bufflen:
                left_off = rec.samples - (self.bufflen - self.samples)
                left = rec.side_copy()
                left.start = rec.samples - left_off
                left.samples = left_off
                top_to = self.bufflen
                if self.triggerSet and left.triggerSet and left.triggered:
                    if left.triggerAt < left.start:
                        self.triggered = True
                        self.triggerAt = self.samples + left.triggerAt
                        left.triggerAt = -1
                        left.triggered = False
                    else:
                        left.triggerAt -= left.start
            else:
                left_off = 0
                left = None
                top_to = self.samples + rec.samples
                if self.triggerSet and rec.triggerSet and rec.triggered:
                    self.triggered = True
                    self.triggerAt = self.samples + rec.triggerAt
            for c in self.buffers.keys():
                try:
                    for key in self.buffers[c].keys():
                        if isinstance(self.buffers[c][key], np.ndarray):
                            self.buffers[c][key][self.samples:top_to] = \
                                rec.buffers[c][key][rec.start:rec.start + rec.samples - left_off]
                        elif isinstance(self.buffers[c][key], bool):
                            self.buffers[c][key] |= rec.buffers[c][key]
                        else:
                            self.buffers[c][key] = rec.buffers[c][key]
                except IndexError:
                    pass
            self.samples = top_to
        except Exception as ex:
            print "records top_up(%d):" % sys.exc_info()[-1].tb_lineno, type(ex), ex.message


    @staticmethod
    def read_chunk(chunk):
        if not isinstance(chunk, tb.group.Group):
            return None
        res = StreamingTapeRecording()
        for attr in chunk._v_parent._v_attrs._v_attrnamesuser:
            res[attr] = chunk._v_parent._v_attrs[attr]
        for attr in chunk._v_attrs._v_attrnamesuser:
            res[attr] = chunk._v_attrs[attr]
        res["index"] = int(chunk._v_name.replace("record", ""))
        res["buffers"] = {}
        for channel in chunk._v_file.listNodes(chunk):
            c = None
            if channel._v_name.startswith("channel"):
                c = int(channel._v_name.replace("channel", ""))
            elif channel._v_name.startswith("port"):
                c = int(channel._v_name.replace("port", "")) | 128
            if c is not None:
                res["buffers"][c] = {}
                for attr in channel._v_attrs._v_attrnamesuser:
                    res["buffers"][c][attr] = channel._v_attrs[attr]
                for a in chunk._v_file.listNodes(channel):
                    res["buffers"][c][a._v_name] = np.array(a.read())
        return res


class RecordsProcessor(multiprocessing.Process):

    def __init__(self, controlq, readq, writeq, watchdogoutq, watchdoginq):
        self._controlq = controlq
        self._readq = readq
        self._writeq = writeq
        self._watchdogInq = watchdoginq
        self._watchdogOutq = watchdogoutq
        self._watchdogEvent = None
        self._watchdogThread = None
        self._filename = None
        self._stats = False
        self._stats_store = dict()
        self._opened = False
        self._memstore = False
        self._records = {}
        self._fhandle = None
        self._writeChapter = ""
        self._writeChapterNode = None
        self._writeChunk = None
        self._readChapter = ""
        self._readChapterNode = None
        self._readChunk = None
        self._limit = 0
        self._waiting = False
        self._waitingChapter = None
        self._stopped = False
        self._purge = False
        super(RecordsProcessor, self).__init__()

    def _watchdog_worker(self, args):
        while not self._watchdogEvent.wait(0.1):
            try:
                keepalive = self._watchdogInq.get(True, 2.0)
            except Queue.Empty:
                keepalive = None
            if keepalive is not None:
                try:
                    self._watchdogOutq.put(True)
                except Exception as ex:
                    print "Dogwatch Send(%d):" % sys.exc_info()[-1].tb_lineno, type(ex), ex.message
            else:
                self._watchdogEvent.set()
        self._controlq.put({"Command": "Exit", "args": None})

    def run(self):
        try:
            self._watchdogEvent = th.Event()
            if self._watchdogEvent.is_set():
                self._watchdogEvent.clear()
            self._watchdogThread = th.Thread(target=self._watchdog_worker, args=(None,))
            ctrl = None
            rec = None
            while True:
                try:
                    ctrl = self._controlq.get(False)
                except Queue.Empty:
                    ctrl = None

                if ctrl is not None and isinstance(ctrl, dict) and "Command" in ctrl:
                    cmd = ctrl["Command"]
                    if cmd == "Next":
                        self._f_next(ctrl["args"])
                    elif cmd == "Last":
                        self._f_last()
                    elif cmd == "Open":
                        self._f_open(ctrl["args"])
                    elif cmd == "Chapters":
                        self._f_chapters()
                    elif cmd == "Stats":
                        self._f_stats()
                    elif cmd == "Watchdog":
                        self._watchdogThread.start()
                    elif cmd == "Exit":
                        self._readq.put(None)
                        break

                if self._opened:
                    received = True
                    try:
                        rec = self._writeq.get(False)
                    except Queue.Empty:
                        received = False
                        rec = None
                    if rec is not None:
                        self._f_record(rec, received)

                if rec is None and ctrl is None:
                    sleep(0.001)
        except Exception as ex:
            print "Tape Proc(%d):" % sys.exc_info()[-1].tb_lineno, type(ex), ex.message
            return
        finally:
            if self._fhandle is not None:
                self._fhandle.flush()
                self._fhandle.close()
            if not self._watchdogEvent.is_set():
                self._watchdogEvent.set()
            self._watchdogThread.join()

    def _f_next(self, args):
        if not self._opened or self._waiting or args["chapter"] is None:
            self._readq.put(None)
            self._waiting = False
        else:
            rec = None
            if self._readChapter != args["chapter"] or self._readChunk is None:
                self._readChapter = args["chapter"]
                if self._memstore:
                    if self._readChapter not in self._records:
                        self._readq.put(None)
                else:
                    self._readChapterNode = None
                    try:
                        self._readChapterNode = self._fhandle.getNode("/", self._readChapter, "Group")
                    except Exception as ex:
                        self._readChapterNode = None
                    if self._readChapterNode is None:
                        self._readq.put(None)
                self._readChunk = 0
            else:
                self._readChunk += 1
            if self._memstore and self._readChapter in self._records:
                if self._readChunk in self._records[self._readChapter]:
                    rec = self._records[self._readChapter][self._readChunk]
                    if args["purge"]:
                        del(self._records[self._readChapter][self._readChunk])
            elif self._readChapterNode is not None:
                try:
                    chunk = self._fhandle.getNode(self._readChapterNode,
                                                  StreamingTape.recfmt % self._readChunk,
                                                  "Group")
                except Exception as ex:
                    chunk = None
                if chunk is not None:
                    rec = StreamingTapeRecording().read_chunk(chunk)

            if rec is not None:
                self._readq.put(rec)
            elif args["wait"] and not self._stopped:
                self._waiting = args["wait"]
                self._purge = args["purge"]
                self._waitingChapter = self._readChapter
                self._readq.put("WAIT")
            else:
                self._readq.put(None)
                self._stopped = False

    def _f_last(self):
        last = None
        try:
            if self._opened and self._writeChunk is not None and self._writeChapter is not None:
                if self._memstore:
                    if self._writeChunk in self._records[self._writeChapter]:
                        last = self._records[self._writeChapter][self._writeChunk]
                elif self._writeChapterNode is not None:
                    chunk = None
                    try:
                        chunk = self._fhandle.getNode(self._writeChapterNode,
                                                      StreamingTape.recfmt % self._writeChunk,
                                                      "Group")
                    except Exception as ex:
                        chunk = None
                    if chunk is not None:
                        last = StreamingTapeRecording.read_chunk(chunk)
        except Exception as ex:
            print "Play Last(%d):" % sys.exc_info()[-1].tb_lineno, type(ex), ex.message
        finally:
            self._readq.put(last)

    def _f_open(self, args):
        if not self._opened:
            self._filename = args["filename"]
            self._title = args["title"]
            if self._title is None or not isinstance(self._title, basestring):
                self._title = strftime("PicoTape-%Y%m%d-%H%M%S")
            self._limit = args["limit"]
            self._overwrite = args["overwrite"]
            if self._filename is not None:
                self._fhandle = None
                error = "OK"
                try:
                    if not os.path.exists(os.path.dirname(self._filename)):
                        error = "Path to %s not found" % self._filename
                    elif not self._overwrite and os.path.exists(self._filename):
                        error = "File %s exists" % self._filename
                    else:
                        self._fhandle = tb.openFile(self._filename, title=self._title, mode="w")
                except Exception as ex:
                    self._fhandle = None
                    error = ex.message
                if self._fhandle is not None:
                    self._opened = True
                self._readq.put(error)
            else:
                self._memstore = True
                self._opened = True
                self._readq.put("OK")
            self._stats = args["stats"] and not self._memstore

    def _f_chapters(self):
        if self._opened:
            if self._memstore:
                self._readq.put(self._records.keys())
            else:
                self._readq.put([node._v_name for node in
                                 self._fhandle.iterNodes("/", classname="Group")])
        else:
            self._readq.put([])

    def _f_record(self, rec, received):
        if rec is not None and isinstance(rec, StreamingTapeRecording):
            if self._stats:
                start_write = time()
                data_len = 0
            if rec.chapter is None:
                if self._writeChapter is not None:
                    rec.chapter = self._writeChapter
                else:
                    rec.chapter = strftime("%Y%m%d_%H%M%S", time())
            if self._writeChapter != rec.chapter or self._writeChunk is None:
                self._writeChapter = rec.chapter
                if self._stopped:
                    self._stopped = False
                if self._memstore:
                    if rec.chapter not in self._records:
                        self._records[rec.chapter] = {}
                else:
                    if self._writeChapterNode is not None:
                        self._writeChapterNode._f_close()
                        self._writeChapterNode = None
                    try:
                        self._writeChapterNode = self._fhandle.getNode("/",
                                                                       self._writeChapter,
                                                                       "Group")
                    except Exception as ex:
                        self._writeChapterNode = None
                    if self._writeChapterNode is None:
                        self._writeChapterNode = self._fhandle.createGroup("/",
                                                                           self._writeChapter,
                                                                           "Group")
                        [self._writeChapterNode._f_setAttr(key, rec[key]) for key in
                         ("chapter", "interval", "units", "mode", "downsample", "device", "serial",
                          "triggerSet", "triggerDirection", "triggerThreshold", "triggerSource")
                         if hasattr(rec, key)]
                self._writeChunk = 0
                if self._stats:
                    self._stats_store = dict()
            else:
                self._writeChunk += 1
            rec["index"] = self._writeChunk
            if self._waiting and rec.chapter == self._waitingChapter:
                self._readq.put(rec)
            if self._opened and self._memstore:
                if not (self._waiting and self._purge):
                    self._records[rec.chapter][self._writeChunk] = rec
                else:
                    self._purge = False
            else:
                chunk = self._fhandle.createGroup(self._writeChapterNode,
                                                  StreamingTape.recfmt % self._writeChunk)
                [chunk._f_setAttr(key, rec[key]) for key in
                 ("timestamp", "samples", "triggerAt", "triggered") if hasattr(rec, key)]
                for c in rec["buffers"].keys():
                    if c & 128:
                        channel = self._fhandle.createGroup(chunk, "port%02d" % (c & 127))
                    else:
                        channel = self._fhandle.createGroup(chunk, "channel%02d" % c)
                    for d in rec["buffers"][c]:
                        if not isinstance(rec["buffers"][c][d], np.ndarray):
                            channel._f_setAttr(d, rec["buffers"][c][d])
                        else:
                            a = self._fhandle.createCArray(channel, d,
                                                           atom=StreamingTape.atom, shape=rec["buffers"][c][d].shape,
                                                           filters=StreamingTape.filters)
                            a[:] = rec["buffers"][c][d][:]
                            if self._stats:
                                data_len += len(rec["buffers"][c][d])
                            a._f_close(True)
                    channel._f_close()
                chunk._f_close()
            self._waiting = False
            if self._stats:
                stop_write = time()
                self._stats_store[self._writeChunk] = {"time": stop_write - start_write, "data_len": data_len}
        elif received and rec is None:
            if self._waiting:
                self._readq.put(None)
                self._waiting = False
            else:
                self._stopped = True

    def _f_stats(self):
        self._readq.put(deepcopy(self._stats_store))
