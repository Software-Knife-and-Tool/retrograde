##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## gra-afch NCS31X driver
##
###########

import ncs31x

gpio = ncs31x.ncs31x()

version = '0.0.1'

conf_dict = None
with open('./gra_afch/gra-afch.conf', 'r') as file:
    conf_dict = json.load(file)
    print(json.dumps(conf_dict))
