"""
 *     Filename: pico_test.py
 *     
 *	   Description:
 *			Example test script.
 * 	  
 *	  @author: mario
 *  
 *    Copyright (C) 2014 - 2017 Pico Technology Ltd. See LICENSE file for terms.
 *
"""

import picosdk.picostatus as st
import numpy as np
from math import pi, sin
from exceptions import IndexError, ZeroDivisionError
import scipy.signal as signal

colors = ((0, 0, 1, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0.7, 0.7, 0, 1),
          (0.66, 0, 1, 1), (0.66, 0.66, 0.66, 1), (0.55, 0.9, 0.9, 1), (1, 0.33, 0.5, 1))
ncolors = [(1 - c[0], 1 - c[1], 1 - c[2], 1) for c in colors]
triggcolor = (0.3, 1, 0.3, 1)
idealcolor = (0.8, 0.5, 0.2, 1)

LOGBUFF = ()
LOGD = None


def p_setlogd(logd):
    global LOGBUFF, LOGD
    LOGD = logd
    if LOGD is not None and len(LOGBUFF) > 0:
        for l in LOGBUFF:
            p_write(l)
        LOGBUFF = ()


def p_write(log):
    global LOGBUFF, LOGD
    if LOGD is None:
        LOGBUFF += (log, )
    else:
        try:
            LOGD.write(log + "\n")
        except OSError:
            pass


def p_warn(msg):
    log = "WARN: %s" % msg
    p_write(log)
    print log


def p_info(msg):
    log = "INFO: %s" % msg
    p_write(log)
    print log


def p_error(msg, end=True):
    log = "ERRO: %s" % msg
    p_write(log)
    print log
    if end:
        exit(1)


def p_assert(title, value=1.0, limit=0.0, result=None):
    if result is not None:
        passed = result
        log = "%s: %s" % ("PASS" if result else "FAIL", title)
    else:
        passed = value <= limit
        log = "%s: %s (%.2f/%.2f)" % ("PASS" if passed else "FAIL", title, value, limit)
    p_write(log)
    print log
    return passed


def error_check(tag, status):
    if status != st.pico_num("PICO_OK"):
        p_error("%s %s" % (tag, st.pico_tag(status)))


def warn_check(tag, status):
    if status != st.pico_num("PICO_OK"):
        p_warn("%s %s" % (tag, st.pico_tag(status)))



