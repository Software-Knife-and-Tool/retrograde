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

from bluedot import BlueDot

VERSION = '0.0.1'

def bluetooth():
    bd = BlueDot()
    bd.wait_for_press()
    print('You pressed the blue dot!')
