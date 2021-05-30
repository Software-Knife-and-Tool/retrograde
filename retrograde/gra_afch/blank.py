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

"""

    docstring

"""

import sys

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retrograde/retrograde/gra_afch')

from ncs31x import blank, ncs31x

VERSION = '0.0.1'

if __name__ == '__main__':
    ncs31x(None)
    blank()
