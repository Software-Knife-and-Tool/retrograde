##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## execute ops
##
###########

"""

    manage retrograde operations

"""

import json
import sys

from threading import Lock
from time import localtime, strftime

# this cleverness brought to you courtesy of having to sudo
sys.path.append(r'/home/lumino/retrograde/retrograde')

import gra_afch
import retro
from events import find, make_event, register

VERSION = '0.0.2'

exec_stack_lock = Lock()
exec_stack = []

def exec_(step):

    print(step)
    
    if 'debug' in step:
        print(step['debug'])
        exec_stack_lock.acquire()
        for i in exec_stack:
            print(i)
        exec_stack_lock.release()
    elif 'repeat' in step:
        def_ = step['repeat']
        op_ = def_['block'] if 'block' in def_ else def_['loop']
        loop_ = 'loop' in def_

        for _ in range(def_['count']):
            exec_op(op_)
    elif 'loop' in step:
        while True:
            exec_op(step['loop'])
    elif 'block' in step:
        for op in step['block']:
            exec_op(op)
    elif 'return' in step:
        return
    elif 'return?' in step:
        if int(exec_stack[-1]) == 0:
            exec_stack.pop()
            return
    elif 'dup' in step:
        exec_stack_lock.acquire()
        tos_ = exec_stack.pop()
        exec_stack.append(tos_)
        exec_stack.append(tos_)
        exec_stack_lock.release()
    elif 'shift' in step:
        def_ = step['shift']
        dir_ = def_['dir']
        count_ = def_['count']
        tos_ = exec_stack[-1]

        exec_stack_lock.acquire()
        for _ in range(count_):
            tos_ = (tos_[1:] if dir_ == 'left' else tos_[:-1]) + ' '
            exec_stack.append(tos_)
        exec_stack_lock.release()
    elif 'pop' in step:
        n_ = step['pop']
        exec_stack_lock.acquire()
        exec_stack.pop(-1 if n_ == 1 else n_)
        exec_stack_lock.release()
    elif 'push' in step:
        exec_stack_lock.acquire()
        exec_stack.append(step['push'])
        exec_stack_lock.release()
    elif 'inc' in step:
        n_ = step['inc']
        exec_stack_lock.acquire()
        exec_stack.append(str(int(exec_stack.pop()) + n_))
        exec_stack_lock.release()
    else:
        return None

    return step

_execs = [exec_]

def register(fn):
    global _exec;
    
    _execs.append(fn)

def exec_op(op):
    global _execs

    for ex in _execs:
        if ex(op):
            return op

    return None
