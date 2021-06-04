##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## retrograde modules
##
###########

"""Module class

Classes:
    Module

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

Misc variables:

    VERSION
    _module_dict

"""

import json
import os
import sys

import event
import gra_afch
import retro
import watchdog

class Module:
    """module class/utility routines
    """

    VERSION = '0.0.1'

    _modules_dict = None

    # modules
    event = None
    gra_afch = None
    retro = None
    watchdog = None

    def path(self, path, file_name):
        return os.path.join(os.path.abspath(os.path.dirname(path)), file_name)

    def events(self, module_name):
        """find module event configuration
        """

        return next((x for x in self._modules_dict['events']
                     if module_name in x), None)

    def find_rotor(self, rotor_name):
        """find rotor
        """

        return next((x for x in self._modules_dict['rotors']
                     if rotor_name in x), None)

    def rotors(self):
        """find rotor definitions
        """

        return self._modules_dict['rotors']

    def __init__(self):
        """instantiate all the modules
        """

        self._modules_dict = []
        with open(self.path(__file__, 'conf.json'), 'r') as file:
            self._modules_dict = json.load(file)

        self.event = event.Event(self)
        self.gra_afch = gra_afch.GraAfch(self)
        self.retro = retro.Retro(self)
        self.watchdog = watchdog.Watchdog(self)
