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
from threading import Lock

##########
#
# events:
#
# { "taarget": MODULE, "type" : TYPE, "id": ID }
#
# MODULE: retrograde, gra_afch, integration
# TYPE:   button1, button2, button3, timer, alarm, ui-control, integration
# ID:     context-based
#
# sneak in a timestamp somehow?
#

_queue = []
_queue_lock = Lock()
_target_locks = []

def _lock_target(target):
    for lock_desc in _target_locks:
        if target == lock_desc[0]:
            return lock_desc[1]

    return None
    
def register(target, lock):
    global _target_locks

    print((target, lock))
    _target_locks.append((target, lock))

def make_event(target, type, id):
    global _queue

    fmt = '{{ "target": "{}", "type": "{}", "id": {} }}'

    with _queue_lock:
        _queue.append(json.loads(fmt.format(target, type, id)));
        _lock_target(target).release()
        
def find(target, lock):
    global _queue

    def in_queue():
        return next((x for x in _queue if target == x['target']), None)

    def_ = None

    print('find: ' + target)
    lock.acquire()
    print('unlocked: ' + target)
    with _queue_lock:
        def_ = in_queue()
        if def_:
            print('found: removing ')
            print(def_)
            _queue.remove(def_)
            if in_queue():
                lock.release()

    print('find: returns')
    print(def_)
    return def_
