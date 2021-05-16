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

# this cleverness due to having to sudo
sys.path.append(r'/home/lumino/lumino/lumino/gra_afch')
from ncs31x import blank, ncs31x
from rotor import rotor_exec, display_date, display_time

VERSION = '0.0.1'

conf_dict = None
_rotor = None

def rotor(rotor_def):
    global _rotor

    if _rotor:
        rotor._exit = True
        _rotor.join()
    _rotor = threading.Thread(target=rotor_exec, args=(rotor_def,))

def gra_afch(rotor_def):
    global _rotor

    def def_thread():
        display_date()
        time.sleep(1)
        blank()
        while True:
            display_time()
            time.sleep(1)

    with open('./gra_afch/gra-afch.conf', 'r') as file:
        conf_dict = json.load(file)
        ncs31x(conf_dict)

    # debugging --
    if rotor_def is None:
        _rotor = threading.Thread(target=def_thread)
    else:
        rotor(rotor_def)

    _rotor.start()
    return conf_dict
