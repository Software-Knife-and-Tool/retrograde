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

import time
import json
import sys
import threading

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/lumino/lumino/gra_afch')
from ncs31x import blank, ncs31x
from rotor import rotor_exec, display_date, display_time

VERSION = '0.0.1'

_conf_dict = None
_rotor = None

def default_rotor():
    if "rotors" in _conf_dict:
        rotors = _conf_dict['rotors']
        if "default" in rotors:
            return rotors['default']

    return None

def rotor(rotor_def):
    global _rotor

    if _rotor:
        rotor._exit = True
        _rotor.join()

    _rotor = threading.Thread(target=rotor_exec, args=(rotor_def,))

def gra_afch():
    global _rotor
    global _conf_dict

    def def_thread():
        display_date()
        time.sleep(1)
        blank()
        while True:
            display_time()
            time.sleep(1)

    with open('./gra_afch/gra-afch.conf', 'r') as file:
        _conf_dict = json.load(file)
        ncs31x(_conf_dict)

    # debugging --
    rotor_def = default_rotor()

    if rotor_def is None:
        _rotor = threading.Thread(target=def_thread)
    else:
        rotor(rotor_def)

    _rotor.start()
    return _conf_dict
