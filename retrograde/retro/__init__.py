##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## retrograde initialization
##
###########

"""Manage GRA-AFCH NCS31X hardware

Classes:
    Retro

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
import sys
import time

# from threading import Thread, Lock

from event import Event
from gra_afch import GraAfch

class Retro:
    """run the rotor thread


    """

    VERSION = '0.0.1'

    _conf_dict = None
    _gra_afch = None
    event = None

    def config(self):
        """run the rotor thread


        """

        return self._conf_dict

    def exec_(self, op):
        """run the rotor thread


        """

        print('retro.exec_')
        print(op)

    def __init__(self):

        self.event = Event()

        def event_proc():
            while True:
                ev = self.event.find_event('retro')
                self.exec_(ev['retro'])

        # with open('./retro/conf.json', 'r') as file:
        #     _conf_dict = json.load(file)

        self._gra_afch = GraAfch(self.event)

        self.event.register_module('retro', event_proc)
