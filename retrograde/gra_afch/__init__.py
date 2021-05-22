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

""" Look at me, I'm a module docstring. """

import json
import sys
import time

from multiprocessing import Process, Lock

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retrograde/retrograde/gra_afch')

from ncs31x import blank, ncs31x
from rotor import rotor_proc
from events import find, event

VERSION = '0.0.1'

_conf_dict = None
_rotor = None
_events = None

def default_rotor():
    if 'rotors' in _conf_dict:
        rotors = _conf_dict['rotors']
        if 'default' in rotors:
            return rotors['default']

    return None

def events():
    def event_proc():
        while True:
            while True:
                event = find('gra_afch')
                if event == None:
                    break
            time.sleep(10)

    _events = Process(target = event_proc)
    _events.start()
    
def rotor(rotor_def):
    global _rotor

    if _rotor:
        rotor._exit = True
        _rotor.join()

    _rotor = Process(target = rotor_proc, args = (rotor_def, ))
    _rotor.start()
    
def gra_afch():
    global _rotor
    global _conf_dict

    with open('./gra_afch/gra-afch.conf', 'r') as file:
        _conf_dict = json.load(file)
        ncs31x(_conf_dict)

    assert default_rotor() != None

    rotor(default_rotor())
    events()

    event('gra_afch', 'hello', 0)
    
    return _conf_dict
