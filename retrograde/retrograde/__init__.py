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

""" look at me! I'm a docstring """

import json
import sys
import time
from multiprocessing import Process, Lock

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retrograde/retrograde/retrograde')

import config
from events import find, register

VERSION = '0.0.1'

_conf_dict = None
_events = None
_lock = None

def retrograde():
    global _conf_dict
    global _events
    global _dict
    global _lock

    def event_proc():
        while True:
            event = find('retrograde', _lock)
            print('(retrograde event:')
            print(event)
            print(')')
            # event loop processing here

    with open('./retrograde/retrograde.conf', 'r') as file:
        _conf_dict = json.load(file)

    _lock = Lock()
    _lock.acquire()
    
    _events = Process(target = event_proc)
    _events.start()

    register('retrograde', 'hello', 0)
    
    return _conf_dict
