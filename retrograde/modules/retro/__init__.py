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

import module

class Retro:
    """the retro module
    """

    VERSION = '0.0.1'

    _conf_dict = None
    _event = None

    def config(self):
        """retro config accessor
        """

        return self._conf_dict

    def exec_(self, op):
        """retor execs
        """

        print('retro.exec_')
        print(op)

    def __init__(self, module_):

        def event_proc():
            while True:
                ev = self._event.find_event('retro')
                self.exec_(ev['retro'])

        with open(module_.path(__file__, 'conf.json'), 'r') as file:
            self._conf_dict = json.load(file)

        self._event = module_.event
        self._event.register_module('retro', event_proc)
