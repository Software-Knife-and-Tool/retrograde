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

import sys
import threading

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/retrograde/retrograde/retrograde/gra_afch')

from ncs31x import blank, ncs31x

VERSION = '0.0.1'

if __name__ == "__main__":
    ncs31x(None)
    blank()
