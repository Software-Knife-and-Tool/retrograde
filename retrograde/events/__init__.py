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
###########

import json
from multiprocessing import Lock

############
#
# events:
#
# { "event": { "source": MODULE, "type" : TYPE, "id": ID } }
#
# SOURCE: retrograde, gra_afch, integration
# TYPE:   button1, button2, button3, timer, alarm, ui-control, integration
# ID: context-based
#
# should sneak in a timestamp somehow
#

_queue = []
_lock = Lock()

def event(source, type, id):
    global _queue

    fmt = '{{ "event": {{ "source": "{}", "type": "{}", "id": {} }} }}'

    with _lock:
        _queue.append(json.loads(fmt.format(source, type, id)));

def find(source):
    global _queue

    def_ = None
    
    with _lock:
        for event in _queue:
            def_ = event['event']
            src_ = def_['source']
            if source == src_:
                _queue.remove(event)
                break

    return def_
