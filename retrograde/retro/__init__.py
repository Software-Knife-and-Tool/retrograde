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

# from threading import Thread, Lock

from event import event, find_event, make_event, register_module
from gra_afch import gra_afch

VERSION = '0.0.1'

_conf_dict = None

def exec_(op):
    print('retro.exec_')
    print(op)

def retro():
    global _conf_dict

    def event_proc():
        while True:
            ev = find_event('retro')
            exec_(ev['retro'])

    # with open('./retro/conf.json', 'r') as file:
    #     _conf_dict = json.load(file)

    event()
    gra_afch()

    register_module('retro', event_proc)
    return _conf_dict
