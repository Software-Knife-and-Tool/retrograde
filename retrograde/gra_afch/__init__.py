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

from threading import Thread, Lock

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retrograde/retrograde/gra_afch')

from ncs31x import blank, ncs31x
from rotor import rotor_proc, exec_
from events import find, make_event, register

VERSION = '0.0.2'

_conf_dict = None

_rotor = None
_events = None
_lock = None

def default_rotor():
    if 'rotors' in _conf_dict:
        rotors = _conf_dict['rotors']
        if 'default' in rotors:
            return rotors['default']

    return None

def default_events():
    if 'events' in _conf_dict:
        return _conf_dict['events']

    return None

def _run_rotor(rotor_def):
    global _rotor

    if _rotor:
        _rotor._exit = True
        _rotor.join()

    _rotor = Thread(target = rotor_proc, args = (rotor_def, ))
    _rotor.start()

def _run_event(ev):
    event = next((x for x in default_events() if ev['type'] in x), None)

    if event:
        exec_(event[ev['type']])
                   
def gra_afch():
    global _rotor
    global _conf_dict
    global _lock

    def event_proc():
        while True:
            event = find('gra_afch', _lock)
            print('gra-afch event:')
            print(event)
            _run_event(event)

    with open('./gra_afch/gra-afch.conf', 'r') as file:
        _conf_dict = json.load(file)
        ncs31x(_conf_dict)

    _run_rotor(default_rotor())

    _lock = Lock();
    _lock.acquire();

    register('gra_afch', _lock)
    make_event('gra_afch', 'hello', 0)

    _events = Thread(target = event_proc)
    _events.start()

    return _conf_dict
