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
from multiprocessing import Process

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retrograde/retrograde/retrograde')

import config
from events import find

VERSION = '0.0.1'

_conf_dict = None
_events = None

def events():
    def event_proc():
        while True:
            while True:
                event = find('retrograde')
                if event == None:
                    break
            time.sleep(1)

    _events = Process(target = event_proc)
    _events.start()

def retrograde():
    global _conf_dict

    with open('./retrograde/retrograde.conf', 'r') as file:
        _conf_dict = json.load(file)

    events()
    return _conf_dict
