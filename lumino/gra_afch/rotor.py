##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## rotors
##
###########

""" the Rotor module implements the rotor programming model """

import wiringpi
import ncs31x
import threading

from time import localtime, strftime

_tube_map = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
_tube_stack = []
_tube_mask = [255 for _ in range(8)]

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
    def scale_(nval):
        return int(nval * (100 / 255))

    ncs31x.update_backlight([scale_(color[0]),
                             scale_(color[1]),
                             scale_(color[2])])

def display_date():
    display_string(strftime('%m%d%y', localtime()))

def display_time():
    display_string(strftime('%H%M%S', ncs31x.sync_time()))

def display_string(digits):
    def get_rep(str_, start):
        bits = (_tube_map[int(str_[start])]) << 20
        bits |= (_tube_map[int(str_[start - 1])]) << 10
        bits |= (_tube_map[int(str_[start - 2])])

        return bits

    # think: individually addressed dots?
    def add_dot_to_rep(bits):
        if _dots:
            bits |= ncs31x.LOWER_DOTS_MASK
            bits |= ncs31x.UPPER_DOTS_MASK
        else:
            bits &= ~ncs31x.LOWER_DOTS_MASK
            bits &= ~ncs31x.UPPER_DOTS_MASK

        return bits

    def fill_buffer(nval, buffer, start):
        buffer[start] = (nval >> 24 & 0xff) & _tube_mask[0]
        buffer[start + 1] = ((nval >> 16) & 0xff) & _tube_mask[1]
        buffer[start + 2] = ((nval >> 8) & 0xff) & _tube_mask[2]
        buffer[start + 3] = (nval & 0xff) & _tube_mask[3]

        return buffer

    left_bits = get_rep(digits, ncs31x.LEFT_REPR_START)
    left_bits = add_dot_to_rep(left_bits)

    buffer = [0 for x in range(8)]
    fill_buffer(left_bits, buffer, ncs31x.LEFT_BUFFER_START)

    right_bits = get_rep(digits, ncs31x.RIGHT_REPR_START)
    right_bits = add_dot_to_rep(right_bits)

    fill_buffer(right_bits, buffer, ncs31x.RIGHT_BUFFER_START)

    ncs31x.display(buffer)

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

#####################
#
#  rotor language:
#
#    name: str         rotor name
#
#      ops:
#        rotors:
#            delay: int         delay for millisecs
#            repeat: { count: int, rotor: [...]
#                               repeat rotor count times
#            rotor: [...]       anonymous rotor definition
#            stop:              stop rotor/pop rotor stack
#
#        display:
#            back: [r, g, b]    backlight color
#            blank: true|false  turn on/off tube power
#            date: str          stuff formatted date to tubes
#            dots: true|false   enable/disable dots
#            mask: int          bit mask for tubes [0..255]
#            time: str          stuff formatted time to tubes
#
#        tube stack:
#            display: null      stuff top of _tube_stack onto tubes
#            pop: null          pop _tube_stack
#            push: str          push digit string on _tube_stack
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
    global _exit, _dots, _tube_mask, _tube_stack

    _dots = ncs31x.config['dots']

    while True:
        for step in rotor:
            if _exit:
                _exit = False
                threading.current_thread.exit()

            # rotors
            if 'delay' in step:
                wiringpi.delay(int(step['delay']))
                continue
            if 'repeat' in step:
                def_ = step['repeat']
                for _ in range(0, def_['count']):
                    rotor_exec(def_['rotor'])
                continue
            if 'rotor' in step:
                rotor_exec(step['rotor'])
                continue
            if 'stop' in step:
                return

            # display
            if 'back' in step:
                update_backlight(step['back'])
                continue
            if 'blank' in step:
                if step['blank']:
                    ncs31x.blank()
                else:
                    ncs31x.unblank()
                continue
            if 'date' in step:
                _tube_stack.append(strftime(step['date'], localtime()))
                continue
            if 'dots' in step:
                _dots = step['dots']
                continue
            if 'time' in step:
                _tube_stack.append(strftime(step['time'], ncs31x.sync_time()))
                continue
            if 'mask' in step:
                mask_ = step['mask']
                for i in range(8):
                    _tube_mask[i] = 255 if mask_ & (2 ** i) else 0
                continue

            # tube stack boogie
            if 'display' in step:
                display_string(_tube_stack[0])
                continue
            if 'pop' in step:
                _tube_stack.pop()
                continue
            if 'push' in step:
                _tube_stack.append(step['push'])
                continue

            print("unimplemented operation")
            print(step)
            threading.current_thread.exit()
