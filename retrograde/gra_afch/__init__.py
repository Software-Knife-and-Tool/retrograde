##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## gra-afch controller
##
###########

""" 

    Look at me, I'm a module docstring.

"""

import json
import sys
import time

from threading import Thread, Lock

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retrograde/retrograde/gra_afch')
from ncs31x import LEFT_REPR_START, LEFT_BUFFER_START
from ncs31x import RIGHT_REPR_START, RIGHT_BUFFER_START
from ncs31x import LOWER_DOTS_MASK, UPPER_DOTS_MASK
from ncs31x import display, blank, unblank, sync_time

from events import find, make_event, register as events_register
from execute import exec_op, exec_stack, exec_stack_lock, register as execute_register

VERSION = '0.0.2'

_conf_dict = None

_rotor = None
_events = None
_lock = None

import wiringpi
import ncs31x
import threading

from time import localtime, strftime

sys.path.append(r'/home/retrograde/retrograde/retrograde/gra_afch')
from ncs31x import blank, ncs31x, backlight

_tube_map = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
_tube_mask = [255 for _ in range(8)]

_rotor = None
_dots = None

# def string_to_color(str_):
#    def ctoi_(nib):#
#        nval = 0
#
#        if nib >= '0' & nib <= '9':
#            nval = nib - '0'
#        elif nib >= 'a' & nib <= 'f':
#            nval = nib - 'a' + 10;
#        elif (nib >= 'A' & nib <= 'F'):
#            nval = nib - 'A' + 10
#        else:
#            nval = -1
#        return nval
#
#    def channel_(msn, lsn):
#        m = ctoi(msn);
#        l = ctoi(lsn);
#
#        return (m < 0 | l < 0) if -1 else (m << 4) + l
#
#    r = channel(str[0], str[1])
#    g = channel(str[2], str[3])
#    b = channel(str[4], str[5])
#
#    return [r, g, b];

def update_backlight(color):
    def scale_(nval):
        return int(nval * (100 / 255))

    backlight([scale_(color[0]),
               scale_(color[1]),
               scale_(color[2])])

def display_string(digits):
    def tubes_(str_, start):
        def num_(ch):
            return 0 if ch == ' ' else int(ch)

        bits = (_tube_map[num_(str_[start])]) << 20
        bits |= (_tube_map[num_(str_[start - 1])]) << 10
        bits |= (_tube_map[num_(str_[start - 2])])

        return bits

    def dots_(bits):
        if _dots:
            bits |= LOWER_DOTS_MASK
            bits |= UPPER_DOTS_MASK
        else:
            bits &= ~LOWER_DOTS_MASK
            bits &= ~UPPER_DOTS_MASK

        return bits

    def fmt_(nval, buffer, start, off):
        buffer[start] = (nval >> 24 & 0xff) & _tube_mask[off]
        buffer[start + 1] = ((nval >> 16) & 0xff) & _tube_mask[off + 1]
        buffer[start + 2] = ((nval >> 8) & 0xff) & _tube_mask[off + 2]
        buffer[start + 3] = (nval & 0xff) & _tube_mask[off + 3]

        return buffer

    buffer = [0 for _ in range(8)]

    left = tubes_(digits, LEFT_REPR_START)
    left = dots_(left)
    fmt_(left, buffer, LEFT_BUFFER_START, 0)

    right = tubes_(digits, RIGHT_REPR_START)
    right = dots_(right)
    fmt_(right, buffer, RIGHT_BUFFER_START, 4)

    display(buffer)

def buttons():
    # auto pin = _MODE_BUTTON_PIN
    ncs31x.init_pin(ncs31x.UP_BUTTON_PIN)
    ncs31x.init_pin(ncs31x.DOWN_BUTTON_PIN)
    ncs31x.init_pin(ncs31x.MODE_BUTTON_PIN)

#    wiringpi.wiringPiISR(_MODE_BUTTON_PIN, _INT_EDGE_RISING,
#                    static unsigned long debounce = 0
#
#                    if ((wiringpi.millis() - debounce) > DEBOUNCE_DELAY):
#
#
#                    [&pin, mutex]() . void:
#                      if (mutex.try_lock()):
#                        pin = MODE_BUTTON_PIN
#                        mutex.unlock()
#                       else
#                        yield()
#                    )
#
#    wiringpi.wiringPiISR(UP_BUTTON_PIN, INT_EDGE_RISING,
#                    [&pin, mutex]() . void:
#                      pin = UP_BUTTON_PIN
#                      mutex.unlock()
#                    )
#
#    wiringpi.wiringPiISR(DOWN_BUTTON_PIN, INT_EDGE_RISING,
#                    [&pin, mutex]() . void:
#                      pin = DOWN_BUTTON_PIN
#                      mutex.unlock()
#                    )

def rotor_proc(rotor):
    """
        rotor_proc(rotor): rotor thread function
             rotor: a list of rotor operations
             returns: void

    """
    
    global _dots

    _dots = _conf_dict['dots']

    exec_op(rotor)
        
def exec_(step):
    global _dots, _tube_mask

    # animation
    if 'delay' in step:
        wiringpi.delay(int(step['delay']))    
    elif 'blank' in step:
        if step['blank']:
            blank()
        else:
            unblank()
    elif 'back' in step:
        update_backlight(step['back'])
    elif 'dots' in step:
        _dots = step['dots']
    elif 'mask' in step:
        # bits 0 and 6 are indicator lamps
        # rightmost number lamp is bit 1
        mask_ = step['mask']
        for i in range(8):
            _tube_mask[i] = 255 if mask_ & (2 ** i) else 0
    elif 'date-time' in step:
        exec_stack_lock.acquire()
        exec_stack.append(strftime(step['date-time'],
                                   sync_time()))
        exec_stack_lock.release()
    elif 'display' in step:
        offset_ = step['display']
        exec_stack_lock.acquire()
        display_string(exec_stack[-offset_])
        exec_stack_lock.release()
    else:
        return None

    return step
        
def default_rotor():
    if 'rotors' in _conf_dict:
        rotors = _conf_dict['rotors']
        if 'default' in rotors:
            return rotors['default']

    return None

def default_events():
    if 'events' in _conf_dict:
        return _conf_dict['events']

    return None

def _run_rotor(rotor_def):
    global _rotor

    if _rotor:
        _rotor._exit = True
        _rotor.join()

    _rotor = Thread(target = rotor_proc, args = (rotor_def, ))
    _rotor.start()


def gra_afch():
    global _rotor, _conf_dict, _lock

    def event_proc():
        while True:
            ev = find('gra_afch', _lock)
            event = next((x for x in default_events() if ev['type'] in x), None)
            if event:
                exec_(event[ev['type']])

    with open('./gra_afch/gra-afch.conf', 'r') as file:
        _conf_dict = json.load(file)
        ncs31x(_conf_dict)

    _run_rotor(default_rotor())

    _lock = Lock();
    _lock.acquire();

    execute_register(exec_)
        
    events_register('gra_afch', _lock)
    make_event('gra_afch', 'hello', 0)

    _events = Thread(target = event_proc)
    _events.start()

    return _conf_dict
