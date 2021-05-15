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
import threading
import sys

sys.path.append(r'/home/lumino/lumino/lumino/gra_afch')
import ncs31x
import rotor

VERSION = '0.0.1'

_conf_dict = None

def rotor_thread():
    rotor.display_date()
    time.sleep(1)
    ncs31x.blank()
    while True:
        rotor.display_time()
        time.sleep(1)

def gra_afch():
    global _conf_dict
    
    with open('./gra_afch/gra-afch.conf', 'r') as file:
        _conf_dict = json.load(file)
        ncs31x.ncs31x(_conf_dict)

        _rotor = threading.Thread(target=rotor_thread, args=())
        _rotor.start()

        return _conf_dict
