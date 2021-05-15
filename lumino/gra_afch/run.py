
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
import ncs31x
import rotor

VERSION = '0.0.1'

with open('./gra-afch.conf', 'r') as file:
    conf_dict = json.load(file)
    ncs31x.ncs31x(conf_dict)
    print(VERSION)
    print(json.dumps(conf_dict))    

rotor.display_date()
time.sleep(1)
ncs31x.blank()
while True:
    rotor.display_time()
    time.sleep(1)
