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

_LEFT_REPR_START = 5
_LEFT_BUFFER_START = 0
_RIGHT_REPR_START = 2
_RIGHT_BUFFER_START = 4

_tube_map = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

_rotor = None

def scale_rgb(nval):
    return int(nval / 2.55)

def string_to_color(str):
    def ctoi(nib):
        nval = 0

        if nib >= '0' & nib <= '9':
            nval = nib - '0'
        elif nib >= 'a' & nib <= 'f':
            nval = nib - 'a' + 10;
        elif (nib >= 'A' & nib <= 'F'):
            nval = nib - 'A' + 10
        else:
            nval = -1
        return nval

    def channel(msn, lsn):
        m = ctoi(msn);
        l = ctoi(lsn);

        return (m < 0 | l < 0) if -1 else (m << 4) + l

    r = channel(str[0], str[1])
    g = channel(str[2], str[3])
    b = channel(str[4], str[5])

    return [r, g, b];

def update_backlight(color):
    ncs31x.update_backlight([scale_rgb(color[0]),
                             scale_rgb(color[1]),
                             scale_rgb(color[2])])

def dot_blink():
    last_time_blink = wiringpi.millis()

    if ((wiringpi.millis() - last_time_blink) >= 1000):
        lastTimeBlink = wiringpi.millis()
        dot_state = not(dot_state)
  
def display_string(digits):
    def get_rep(str, start):
        bits = 0

        bits = (_tube_map[int(str[start])]) << 20
        bits |= (_tube_map[int(str[start - 1])]) << 10
        bits |= (_tube_map[int(str[start - 2])])
  
        return bits

    def add_blink_to_rep(bits):
#        if dotState:
#            bits &= ~_LOWER_DOTS_MASK
#            bits &= ~_UPPER_DOTS_MASK
#        else:
#            bits |= _LOWER_DOTS_MASK
#            bits |= _UPPER_DOTS_MASK
  
        return bits

    def fill_buffer(nval, buffer, start):
        buffer[start] = (nval >> 24 & 0xff)
        buffer[start + 1] = (nval >> 16) & 0xff
        buffer[start + 2] = (nval >> 8) & 0xff
        buffer[start + 3] = nval & 0xff

        return buffer;

#    if cfg.dotState
#      dot_blink()

    left_bits = get_rep(digits, _LEFT_REPR_START)
    left_bits = add_blink_to_rep(left_bits)

    buffer = [x for x in range(8)]
    fill_buffer(left_bits, buffer, _LEFT_BUFFER_START)

    right_bits = get_rep(digits, _RIGHT_REPR_START)
    right_bits = add_blink_to_rep(right_bits)
    
    fill_buffer(right_bits, buffer, _RIGHT_BUFFER_START)

    ncs31x.display(buffer)

def display_date():
    display_string(strftime('%m%d%y', localtime()))

def display_time():
    display_string(strftime('%H%M%S', ncs31x.sync_time()))
    
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
#        blank: bool        [on|off] turn on/off tubes
#        date: fmt-str      [fmt-str] push formatted date to tubes 
#        time: fmt-str      [fmt-str] push formatted time to tubes
#        delay: int         [n] delay for n millisecs
#        tube: {...}        [n, on|off, digit]
#        display: str       [digits] digit string on tubes
#        back: [...]        [r, g, b] backlight color
#        rotor: [...]       anonymous rotor
#        exit:              stop rotoring/pop rotor stack
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

    while True:
        for step in rotor:
            if _exit:
                _exit = False
                threading.current_thread.exit()
            if 'exit' in step:
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
            if 'time' in step:
                display_string(strftime(step['time'], ncs31x.sync_time()))
                continue
            if 'tube' in step:
                ncs31x.tube(step['tube'])
                continue
            if 'display' in step:
                display_string(step['display'])
                continue
            if 'rotor' in step:
                rotor_exec(step['rotor'])
                continue
