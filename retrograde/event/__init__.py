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

"""Manage retrograde events

See module gra-afch for display events.
See module retro for system events.

Classes:

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

    event()
    find_event(module)
    make_event(module, type_, arg)
    register_module(module, fn)
    send_event(ev)

Misc variables:

    VERSION
    _conf_dict
    _modules
    _modules_lock
    _queue
    _queue_lock

"""

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

def _lock_module(module):
    global _modules

    with _modules_lock:
        for lock_desc in _modules:
            module_, lock_, _ = lock_desc
            if module == module_:
                return lock_

    assert False
    return None

def register_module(module_, fn):
    """register a module event thread

       create a per-module event thread and lock
       and bind them to module.

       the module event thread waits on the lock
       by calling find_event until somebody does
       a send_event with their tag.

       there shouldn't be any events already on
       queue for a unregistered module, if we want
       to allow that we can grovel through the
       queue and set the lock state accordingly
       like find_event.

    """

    global _modules, _modules_lock

    with _modules_lock:
        lock_ = Lock()
        lock_.acquire()
        thread_ = Thread(target = fn)
        _modules.append((module_, lock_, thread_))

        thread_.start()

def find_event(module):
    """find a module event

       unless there are one or more events on
       the queue for module, wait until
       send_event releases the wait lock.

    """

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

def send_event(ev):
    """push an event on the event queue

       release the module event lock if
       it is already locked.

       module locks are only changed
       with the queue lock held, so
       this is safe.

    """

    global _queue, _queue_lock

    module = list(ev)[0]
    lock = _lock_module(module)

    if _queue_lock.locked():
        print('sleepytime')
    with _queue_lock:
        _queue.append(ev)
        if lock.locked():
            lock.release()

def make_event(module, type_, arg):
    global _queue

    fmt = '{{ "{}": {{ "{}": "{}" }} }}'

    send_event(json.loads(fmt.format(module, type_, arg)))

def _exec(op):
    step = op['exec']

    if 'repeat' in step:
        def_ = step['repeat']
        count_ = def_['count']

        if isinstance(count_, bool):
            while count_:
                for op_ in def_['block']:
                    send_event(op_)
        elif isinstance(count_, int):
            for _ in range(count_):
                for op_ in def_['block']:
                    send_event(op_)
        else:
            assert False
    elif 'block' in step:
        for op_ in step['block']:
            send_event(op_)
    else:
        assert False

def event():
    global _queue_lock, _queue
    global _modules_lock, _modules

    def event_proc():
        while True:
            ev = find_event('event')
            _exec(ev['event'])

    # with open('./event/conf.json', 'r') as file:
    #    _conf_dict = json.load(file)

    _queue_lock = Lock()
    _queue = []

    _modules_lock = Lock()
    _modules = []

    register_module('event', event_proc)
