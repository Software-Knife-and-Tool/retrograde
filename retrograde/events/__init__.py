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
from multiprocessing import Lock

##########
#
# events:
#
# { "event": { "source": MODULE, "type" : TYPE, "id": ID } }
#
# MODULE: retrograde, gra_afch, integration
# TYPE:   button1, button2, button3, timer, alarm, ui-control, integration
# ID:     context-based
#
# sneak in a timestamp somehow?
#

_queue = []
_queue_lock = Lock()

def register(source, type, id):
    global _queue

    fmt = '{{ "event": {{ "source": "{}", "type": "{}", "id": {} }} }}'
    with _queue_lock:
        _queue.append(json.loads(fmt.format(source, type, id)));

def find(source, lock):
    global _queue

    def in_queue(source):
        for event in _queue:
            def_ = event['event']
            src_ = def_['source']
            if source == src_:
                return def_

        return None

    _def = None

    lock.acquire()
    with _queue_lock:
        def_ = in_queue(source)
        if def_:
            print(def_)
            _queue.remove(def_)
            if in_queue(source):
                lock.release()

    return def_
