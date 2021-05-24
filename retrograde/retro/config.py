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

     look at me! I'm a docstring!

"""

import json
import sys

sys.path.append(r'/home/lumino/retrograde/retrograde/retro')
import events

from bluedot import BlueDot

VERSION = '0.0.1'

_conf_dict = None

def bluetooth():
    bd = BlueDot()
    bd.wait_for_press()
    print("You pressed the blue dot!")
