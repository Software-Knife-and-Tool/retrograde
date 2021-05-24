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

"""

    look at me! I'm a docstring

"""

import json
import sys
import time

from threading import Thread, Lock

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retro/retro/retro')
from events import find, make_event, register

VERSION = '0.0.1'

_conf_dict = None
_events = None
_lock = None

def retro():
    global _conf_dict, _events, _lock

    def event_proc():
        while True:
            event = find('retro', _lock)

    with open('./retro/retrograde.conf', 'r') as file:
        _conf_dict = json.load(file)

    _lock = Lock()
    _lock.acquire()
    
    _events = Thread(target = event_proc)
    _events.start()

    register('retro', _lock)
    
    make_event('retro', 'hello', 0)
    
    return _conf_dict
