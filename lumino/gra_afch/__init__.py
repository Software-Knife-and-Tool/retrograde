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

sys.path.append(r'/home/lumino/lumino/lumino/gra_afch')
import ncs31x
import rotor

VERSION = '0.0.1'

conf_dict = None

def rotor_thread():
    rotor.display_date()
    time.sleep(1)
    ncs31x.blank()
    while True:
        rotor.display_time()
        time.sleep(1)

def gra_afch():
    with open('./gra_afch/gra-afch.conf', 'r') as file:
        conf_dict = json.load(file)
        ncs31x.ncs31x(conf_dict)
        print(VERSION)
        print(json.dumps(conf_dict))    

        _rotor = threading.Thread(target=rotor_thread, args=())
        _rotor.start()

gra_afch()
