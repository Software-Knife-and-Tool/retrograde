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

See module gra-afch for display/RTC events.
See module retro for system events.

Classes:
    Event

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

    event()
    find_event(module)
    make_event(module, type_, arg)
    register(module, fn)
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

class Event:
    """the event class
    """

    VERSION = '0.0.3'

    _conf_dict = None

    _queue = None
    _queue_lock = None

    _modules_lock = None
    _modules = None

    def _lock_module(self, module):

        with self._modules_lock:
            for lock_desc in self._modules:
                module_, lock_, _ = lock_desc
                if module == module_:
                    return lock_

        assert False
        return None

    def register(self, module_, fn):
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

        with self._modules_lock:
            lock_ = Lock()
            lock_.acquire()
            thread_ = Thread(target = fn)
            self._modules.append((module_, lock_, thread_))

            thread_.start()

    def find_event(self, module):
        """find a module event

           unless there are one or more events on
           the queue for module, wait until
           send_event releases the wait lock.

        """

        def in_queue():
            return next((x for x in self._queue if module in x), None)

        def_ = None

        lock = self._lock_module(module)
        lock.acquire()

        with self._queue_lock:
            def_ = in_queue()
            if def_:
                self._queue.remove(def_)
            if in_queue() and lock.locked():
                lock.release()

        return def_

    def send_event(self, ev):
        """push an event on the event queue

            release the module event lock if
            it is already locked.

            module locks are only changed
            with the queue lock held, so
            this is safe.

        """

        module = list(ev)[0]
        lock = self._lock_module(module)

        with self._queue_lock:
            self._queue.append(ev)
            if lock.locked():
                lock.release()

    def make_event(self, module, type_, arg):
        """find a module event

           unless there are one or more events on
           the queue for module, wait until
           send_event releases the wait lock.

        """

        fmt = '{{ "{}": {{ "{}": "{}" }} }}'

        self.send_event(json.loads(fmt.format(module, type_, arg)))

    def exec_(self, op):
        """find a module event

           unless there are one or more events on
           the queue for module, wait until
           send_event releases the wait lock.

        """

        step = op['exec']

        if 'repeat' in step:
            def_ = step['repeat']
            count_ = def_['count']

            if isinstance(count_, bool):
                while count_:
                    for op_ in def_['block']:
                        self.send_event(op_)
            elif isinstance(count_, int):
                for _ in range(count_):
                    for op_ in def_['block']:
                        self.send_event(op_)
            else:
                assert False
        elif 'block' in step:
            for op_ in step['block']:
                self.send_event(op_)
        else:
            assert False

    def config(self):
        return self._conf_dict

    def __init__(self, module):
        """find a module event

           unless there are one or more events on
           the queue for module, wait until
           send_event releases the wait lock.

        """

        def event_proc():
            while True:
                ev = self.find_event('event')
                self.exec_(ev['event'])

        self._conf_dict = []
        with open(module.path(__file__, 'conf.json'), 'r') as file:
            self._conf_dict = json.load(file)

        self._queue_lock = Lock()
        self._queue = []

        self._modules_lock = Lock()
        self._modules = []

        self.register('event', event_proc)
