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

"""Manage GRA-AFCH NCS31X hardware

See module ncs31x for display/clock interface.

Classes:
    GraAfch

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

    buttons()
    default_rotor()
    display_string(digits)
    exec_(op)
    gra_afch()
    run_rotor(rotor_def)
    update_backlight(color)

Misc variables:

    VERSION
    _conf_dict
    _dots
    _lock
    _rotor
    _tube_mask

"""

import json
import time
import wiringpi

from time import localtime, strftime
from datetime import datetime
from threading import Thread, Lock, Timer

from .ncs31x import Ncs31x

class GraAfch:
    """run the rotor thread
    """

    VERSION = '0.0.3'

    _conf_dict = None

    _rotor = None
    _lock = None
    _dots = None
    _ncs31x = None

    _tube_mask = [255 for _ in range(8)]
    _toggle = None

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

    def update_backlight(self, color):
        """change the backlight color
        """

        def scale_(nval):
            return int(nval * (100 / 255))

        self._ncs31x.backlight([scale_(color[0]),
                                scale_(color[1]),
                                scale_(color[2])])

    def display_string(self, digits):
        """stuff the tubes from decimal string
        """

        def tubes_(str_, start):
            tube_map_ = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]

            def num_(ch):
                return 0 if ch == ' ' else int(ch)

            bits = (tube_map_[num_(str_[start])]) << 20
            bits |= (tube_map_[num_(str_[start - 1])]) << 10
            bits |= (tube_map_[num_(str_[start - 2])])

            return bits

        def dots_(bits):
            if self._dots:
                bits |= Ncs31x.LOWER_DOTS_MASK
                bits |= Ncs31x.UPPER_DOTS_MASK
            else:
                bits &= ~Ncs31x.LOWER_DOTS_MASK
                bits &= ~Ncs31x.UPPER_DOTS_MASK

            return bits

        def fmt_(nval, buffer, start, off):
            buffer[start] = (nval >> 24 & 0xff) & self._tube_mask[off]
            buffer[start + 1] = ((nval >> 16) & 0xff) & self._tube_mask[off + 1]
            buffer[start + 2] = ((nval >> 8) & 0xff) & self._tube_mask[off + 2]
            buffer[start + 3] = (nval & 0xff) & self._tube_mask[off + 3]

            return buffer

        buffer = [0 for _ in range(8)]

        left = tubes_(digits, Ncs31x.LEFT_REPR_START)
        left = dots_(left)
        fmt_(left, buffer, Ncs31x.LEFT_BUFFER_START, 0)

        right = tubes_(digits, Ncs31x.RIGHT_REPR_START)
        right = dots_(right)
        fmt_(right, buffer, Ncs31x.RIGHT_BUFFER_START, 4)

        self._ncs31x.display(buffer)

    def buttons(self):
        """button events
        """

        # auto pin = _MODE_BUTTON_PIN
        self._ncs31x.init_pin(self._ncs31x.UP_BUTTON_PIN)
        self._ncs31x.init_pin(self._ncs31x.DOWN_BUTTON_PIN)
        self._ncs31x.init_pin(self._ncs31x.MODE_BUTTON_PIN)

#    wiringpi.wiringPiISR(_MODE_BUTTON_PIN, _INT_EDGE_RISING,
#                    static unsigned long debounce = 0
#
#                    if ((wiringpi.millis() - debounce) > DEBOUNCE_DELAY):
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

    def exec_(self, op):
        """gra-afch operations
        """
        step = op['exec']

        # this is wrong
        if not self._toggle:
            self._ncs31x.blank(not self._toggle)
        elif 'delay' in step:
            wiringpi.delay(int(step['delay']))
        elif 'blank' in step:
            self._ncs31x.blank(step['blank'])
        elif 'back' in step:
            self.update_backlight(step['back'])
        elif 'dots' in step:
            self._dots = step['dots']
        elif 'mask' in step:
            # bits 0 and 6 are indicator lamps
            # rightmost number lamp is bit 1
            mask_ = step['mask']
            for i in range(8):
                self._tube_mask[i] = 255 if mask_ & (2 ** i) else 0
        elif 'date-time' in step:
            self.display_string(
                strftime(step['date-time'], self._ncs31x.read_rtc()))
        elif 'display' in step:
            self.display_string(step['display'])
        elif 'sync' in step:
            self._ncs31x.write_rtc(localtime())
        else:
            assert False

    def _events(self):
        if 'events' in self._conf_dict:
            return self._conf_dict['events']

        return None

    def config(self):
        return self._conf_dict

    def _run_rotor(self, rotor_def):
        """run the rotor thread
        """

        def rotor_proc(rotor):
            self._dots = self._conf_dict['dots']
            self._event.send_event(rotor)

        if self._rotor:
            self._rotor._exit = True
            self._rotor.join()

        self._rotor = Thread(target = rotor_proc, args = (rotor_def, ))
        self._rotor.start()

    def __init__(self, retro_):
        """initialize the gra-afch module

            register with the event module
            read the config file
            crank up the default rotor
        """

        event = retro_.event

        def event_proc():
            """grab one of our events off the queue

               if it's an exec, do it.

               if it's an event, go look it up in our
               event config and send whatever it maps
               to back to the queue.
            """

            while True:
                event_ = self._event.find_event('gra-afch')['gra-afch']
                type_ = list(event_)[0]

                if type_ == 'exec':
                    self.exec_(event_)

                elif type_ == 'event':
                    arg_ = event_['event']
                    # print('event!: ', end='')
                    # print(event_)
                    # print(datetime.now().strftime('%H:%M:%S:%f'))

                    if 'toggle' == arg_:
                        self._toggle = not self._toggle
                    elif 'timer' == arg_:
                        def timer_():
                            Timer(event_['timer'] / 1000, timer_).start()
                    else:
                        for ev in retro_.events('gra-afch'):
                            if arg_ == list(ev)[0]:
                                self._event.send_event(ev[arg_])
                else:
                    assert False

        self._event = event
        self._event.register('gra-afch', event_proc)

        self._conf_dict = []
        with open(retro_.path(__file__, 'conf.json'), 'r') as file:
            self._conf_dict = json.load(file)

        self._toggle = True
        # does ncs31x need the configuration dictionary?
        self._ncs31x = Ncs31x(self._conf_dict)

        self._run_rotor(retro_.find_rotor('default')['default'])
