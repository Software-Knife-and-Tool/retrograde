##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## watchdog module
##
###########

"""retrograde timers

Classes:
    Watchdog

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

from time import localtime, strftime
from threading import Thread, Lock, Timer

import module

class Watchdog:
    """run the rotor thread
    """

    VERSION = '0.0.3'

    _conf_dict = None

    def exec_(self, op):
        """timer operations
        """

        step = op['exec']

        if 'timer' in step:
            print('timer')
            print(step)
            def timer_():
                print('ding')
                self._event.make_event('gra-afch', 'event', 'timer')
            Timer(step['timer'] / 1000, timer_).start()

            # Timer(step['timer'] / 1000,
            #      lambda : self._event.make_event('gra-afch',
            #                                      'event',
            #                                      'timer')).start()
        else:
            assert False

    def _events(self):
        if 'events' in self._conf_dict:
            return self._conf_dict['events']

        return None

    def __init__(self, module_):
        """initialize the timer module

            read the config file
            register with the event module
        """

        def _event_proc():
            """grab one of our events off the queue

               if it's an exec, do it.

               if it's an event, go look it up in our
               event config and send whatever it says
               to back to the queue.
            """

            while True:
                event_ = self._event.find_event('watchdog')['timer']
                etype_ = list(event_)[0]
                if etype_ == 'event':
                    for ev in module_.events('timer'):
                        if event_['event'] == list(ev)[0]:
                            self._event.send_event(ev[event_['event']])
                elif etype_ == 'exec':
                    self.exec_(event_)
                else:
                    assert False

        self._event = module_.event

        with open(module_.path(__file__, 'conf.json'), 'r') as file:
            self._conf_dict = json.load(file)

        self._event.register('watchdog', _event_proc)
