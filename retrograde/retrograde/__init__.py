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

VERSION = '0.0.1'

_conf_dict = None

def retrograde():
    global _conf_dict

    with open('./retrograde/retrograde.conf', 'r') as file:
        _conf_dict = json.load(file)

    return _conf_dict
