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
_tube_mask = [255 for _ in range(8)]

_display_stack = []
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

    ncs31x.update_backlight([scale_(color[0]),
                             scale_(color[1]),
                             scale_(color[2])])

def display_date():
    display_string(strftime('%m%d%y', localtime()))

def display_time():
    display_string(strftime('%H%M%S', ncs31x.sync_time()))

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
            bits |= ncs31x.LOWER_DOTS_MASK
            bits |= ncs31x.UPPER_DOTS_MASK
        else:
            bits &= ~ncs31x.LOWER_DOTS_MASK
            bits &= ~ncs31x.UPPER_DOTS_MASK

        return bits

    def fmt_(nval, buffer, start, off):
        buffer[start] = (nval >> 24 & 0xff) & _tube_mask[off]
        buffer[start + 1] = ((nval >> 16) & 0xff) & _tube_mask[off + 1]
        buffer[start + 2] = ((nval >> 8) & 0xff) & _tube_mask[off + 2]
        buffer[start + 3] = (nval & 0xff) & _tube_mask[off + 3]

        return buffer

    buffer = [0 for _ in range(8)]

    left = tubes_(digits, ncs31x.LEFT_REPR_START)
    left = dots_(left)
    fmt_(left, buffer, ncs31x.LEFT_BUFFER_START, 0)

    right = tubes_(digits, ncs31x.RIGHT_REPR_START)
    right = dots_(right)
    fmt_(right, buffer, ncs31x.RIGHT_BUFFER_START, 4)

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

def rotor_exec(rotor):
    """
        rotor_exec(rotor): rotor thread function
             rotor: a list of rotor operations
             returns: void
    """
    global _dots

    _exit = None
    _dots = ncs31x.config['dots']

    def exec_(rotor, loop):
        global _dots, _tube_mask, _display_stack

        while True:
            for step in rotor:
                if _exit:
                    # _exit = False
                    threading.current_thread.exit()

                # debugging
                if 'debug' in step:
                    print(step['debug'])
                    for i in _display_stack:
                        print(i)
                    continue

                # rotors
                if 'delay' in step:
                    wiringpi.delay(int(step['delay']))
                    continue
                if 'repeat' in step:
                    def_ = step['repeat']
                    op_ = def_['block'] if 'block' in def_ else def_['loop']
                    loop_ = 'loop' in def_

                    for _ in range(def_['count']):
                        exec_(op_, loop_)
                    continue
                if 'loop' in step:
                    exec_(step['loop'], True)
                    continue
                if 'block' in step:
                    exec_(step['block'], False)
                    continue
                if 'return' in step:
                    return
                if 'return?' in step:
                    if int(_display_stack[-1]) == 0:
                        _display_stack.pop()
                        return
                    continue

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
                if 'dots' in step:
                    _dots = step['dots']
                    continue
                if 'mask' in step:
                    # bits 0 and 6 are indicator lamps
                    # rightmost number lamp is bit 1
                    mask_ = step['mask']
                    for i in range(8):
                        _tube_mask[i] = 255 if mask_ & (2 ** i) else 0
                    continue

                # tube stack boogie
                if 'date-time' in step:
                    _display_stack.append(strftime(step['date-time'],
                                                ncs31x.sync_time()))
                    continue
                if 'display' in step:
                    offset_ = step['display']
                    display_string(_display_stack[-offset_])
                    continue
                if 'dup' in step:
                    tos_ = _display_stack.pop()
                    _display_stack.append(tos_)
                    _display_stack.append(tos_)
                    continue
                if 'shift' in step:
                    def_ = step['shift']
                    dir_ = def_['dir']
                    count_ = def_['count']
                    tos_ = _display_stack[-1]

                    for _ in range(count_):
                        tos_ = (tos_[1:] if dir_ == 'left' else tos_[:-1]) + ' '
                    _display_stack.append(tos_)
                    continue
                if 'pop' in step:
                    n_ = step['pop']
                    _display_stack.pop(-1 if n_ == 1 else n_)
                    continue
                if 'push' in step:
                    _display_stack.append(step['push'])
                    continue
                if 'inc' in step:
                    n_ = step['inc']
                    _display_stack.append(str(int(_display_stack.pop()) + n_))
                    continue

                print('unimplemented operation')
                print(step)

            if not loop:
                break

    exec_(rotor, True)
