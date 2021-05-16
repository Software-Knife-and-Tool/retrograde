##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## lumino initialization
##
###########

import json

VERSION = '0.0.1'

_conf_dict = None

def lumino():
    global _conf_dict
        
    with open('./lumino/lumino.conf', 'r') as file:
        _conf_dict = json.load(file)
        
    return _conf_dict
