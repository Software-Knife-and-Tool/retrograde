##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## NCS31X rotor
##
###########

import wiringpi
import ncs31x

from time import time, localtime, strftime

_tube_map = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

_rotor = None
_dots = None

#
# use this if we want to accept
# hex rrggbb strings in json
#

# def string_to_color(str):
#    def ctoi(nib):
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
#    def channel(msn, lsn):
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
    def _scale(nval):
        return int(nval * (100 / 255))

    ncs31x.update_backlight([_scale(color[0]),
                             _scale(color[1]),
                             _scale(color[2])])

def display_date():
    display_string(strftime('%m%d%y', localtime()))

def display_time():
    display_string(strftime('%H%M%S', ncs31x.sync_time()))
    
def display_string(digits):
    def get_rep(str, start):
        bits = (_tube_map[int(str[start])]) << 20
        bits |= (_tube_map[int(str[start - 1])]) << 10
        bits |= (_tube_map[int(str[start - 2])])
  
        return bits

    def add_dot_to_rep(bits):
        if _dots:
            bits |= ncs31x._LOWER_DOTS_MASK
            bits |= ncs31x._UPPER_DOTS_MASK
        else:
            bits &= ~ncs31x._LOWER_DOTS_MASK
            bits &= ~ncs31x._UPPER_DOTS_MASK
            
        return bits

    def fill_buffer(nval, buffer, start):
        buffer[start] = (nval >> 24 & 0xff)
        buffer[start + 1] = (nval >> 16) & 0xff
        buffer[start + 2] = (nval >> 8) & 0xff
        buffer[start + 3] = nval & 0xff

        return buffer;

    left_bits = get_rep(digits, ncs31x._LEFT_REPR_START)
    left_bits = add_dot_to_rep(left_bits)

    buffer = [x for x in range(8)]
    fill_buffer(left_bits, buffer, ncs31x._LEFT_BUFFER_START)

    right_bits = get_rep(digits, ncs31x._RIGHT_REPR_START)
    right_bits = add_dot_to_rep(right_bits)
    
    fill_buffer(right_bits, buffer, ncs31x._RIGHT_BUFFER_START)

    ncs31x.display(buffer)

def buttons():
    # auto pin = _MODE_BUTTON_PIN
    init_pin(_UP_BUTTON_PIN)
    init_pin(_DOWN_BUTTON_PIN)
    init_pin(_MODE_BUTTON_PIN)

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

#####################
#
#  rotor definition:
#
#    name: str         rotor name
#
#      ops:
#        back: [...]        [r, g, b] backlight color
#        blank: bool        [on|off] turn on/off tubes
#        date: fmt-str      [fmt-str] push formatted date to tubes 
#        delay: int         [n] delay for n millisecs
#        display: str       [digits] digit string on tubes
#        stop:              stop rotor/pop rotor stack
#        repeat: { count: n, rotor: [...]
#                           repeat rotor n times
#        rotor: [...]       anonymous rotor
#        time: fmt-str      [fmt-str] push formatted time to tubes
#        tube: {...}        [n, on|off, digit]
#
#  json:
#    "rotors" : {
#        "name" : {
#                   "op": ...,
#                 },
#    },
#

_exit = None
def rotor_exec(rotor):
    global _exit
    global _dots

    _dots = ncs31x.config['dots']
    while True:
        for step in rotor:
            if _exit:
                _exit = False
                threading.current_thread.exit()
            if 'stop' in step:
                return
            if 'back' in step:
                update_backlight(step['back'])
                continue
            if 'delay' in step:
                wiringpi.delay(int(step['delay']))
                continue
            if 'blank' in step:
                if step['blank']:
                    ncs31x.blank()
                else:
                    ncs31x.unblank()
                continue
            if 'date' in step:
                display_string(strftime(step['date'], localtime()))
                continue
            if 'dots' in step:
                _dots = step['dots']
                continue
            if 'time' in step:
                display_string(strftime(step['time'], ncs31x.sync_time()))
                continue
            if 'tube' in step:
                ncs31x.tube(step['tube'])
                continue
            if 'display' in step:
                display_string(step['display'])
                continue
            if 'repeat' in step:
                _def = step['repeat']
                for i in range(0, _def['count']):
                    rotor_exec(_def['rotor'])
                continue
            if 'rotor' in step:
                rotor_exec(step['rotor'])
                continue
