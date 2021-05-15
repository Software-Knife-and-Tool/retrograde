##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## rotor language
##
###########

# rotor language:
#
#      name: str         rotor name
#
#      blank [...]       [on|off] turn on/off tubes
#      date [...]        [fmt-str] push formatted date to tubes 
#      time [...]        [fmt-str] push formatted time to tubes
#      delay [...]       [n] delay for n millisec
#      tube [...]        [n, on|off, digit]
#      display [...]     [digits] digit string on tubes
#
#      exit              stop rotoring/pop rotor stack
#
#  json:
#    "rotor" : {
#                "name" : "...",
#                "cmd": [ ... ],
#              }
      
_rotor_defs = []

def _name(str):
    return

def _blank(on):
    return

def _date(fmt):
    return

def _time(fmt):
    return

def _delay(ms):
    return

def _tube(n, on, digit):
    return

def _display(digits):
    return

def _exit():
    return

# takes a rotor def dict
# adds to rotor namespace
def rotor(def_dict):
    global _rotor_defs

    _rotor_defs.append(def_dict)
    return
