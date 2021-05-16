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

def lumino():
    with open('./lumino/lumino.conf', 'r') as file:
        _conf_dict = json.load(file)
        # print(json.dumps(_conf_dict))
        
    return _conf_dict

lumino()
