##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## events
##
##########

import json
import sys
from threading import Thread, Lock
from time import localtime, strftime

VERSION = '0.0.3'

##########
#
# event format:
#
# { "module": { "event" : arg } }
#
# module: event, retro, gra-afch, integration
# event:  button, timer, alarm, ui-control, integration, exec
# arg:    context-based
#
# sneak in a timestamp somehow?
#

_conf_dict = None

_queue = None
_queue_lock = None

_modules_lock = None
_modules = None

####
#
# external interfaces
#
####

def exec_(op):
    step = op['exec']
        
    if 'repeat' in step:
        def_ = step['repeat']
        for _ in range(def_['count']):
            for op_ in def_['block']:
                send_event(op_)            
    elif 'loop' in step:
        while True:
            for op_ in step['loop']:
                send_event(op_)
    elif 'block' in step:
        for op_ in step['block']:
            send_event(op_)
    else:
        assert(False)

def exec_lock():
    pass

def _lock_module(module):
    global _modules

    _modules_lock.acquire()
    for lock_desc in _modules:
        module_, lock, _ = lock_desc
        if module == module_:
            _modules_lock.release()
            return lock

    print("-- _lock_modules failure")
    print(_modules)
    print('-- for module')
    print(module)
    
    assert(False)
    return None
    
def register(module, fn):
    global _modules, _modules_lock

    _modules_lock.acquire()
    
    lock = Lock();
    lock.acquire();
    
    thread = Thread(target = fn)

    _modules.append((module, lock, thread))
    _modules_lock.release()

    thread.start()
        
def send_event(event):
    global _queue, _queue_lock

    with _queue_lock:
        _queue.append(event)
        module = list(event)[0]
        lock = _lock_module(module)
        if lock.locked():
            lock.release()
        
def make_event(module, type, arg):
    global _queue

    fmt = '{{ "{}": {{ "{}": "{}" }} }}'

    send_event(json.loads(fmt.format(module, type, arg)))

def find_event(module):
    global _queue, _queue_lock

    def in_queue():
        return next((x for x in _queue if module in x), None)

    def_ = None

    lock = _lock_module(module)
    lock.acquire()

    with _queue_lock:
        def_ = in_queue()
        if def_:
            _queue.remove(def_)
            if in_queue() and lock.locked():
                lock.release()

    return def_

def event():
    global _queue_lock, _queue
    global _modules_lock, _modules

    def event_proc():
        while True:
            ev = find_event('event')
            # event = next((x for x in default_events() if ev['type'] in x), None)
            exec_(ev['event'])

    # with open('./event/conf.json', 'r') as file:
    #    _conf_dict = json.load(file)

    _queue_lock = Lock()
    _queue = []

    _modules_lock = Lock()
    _modules = []

    register('event', event_proc)    
