##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## lumino controller
##
###########

import json

VERSION = '0.0.1'

with open('./lumino.conf', 'r') as file:
    conf_dict = json.load(file)
    print(VERSION)
    print(json.dumps(conf_dict))
