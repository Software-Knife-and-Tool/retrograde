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

"""Manage GRA-AFCH NCS31X hardware

Classes:
    Retro

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

Misc variables:

    VERSION
    _conf_dict

"""

import json
import os
import socket
import sys
import time

from datetime import datetime

from flask_socketio import SocketIO
from threading import Thread, Lock, Timer

import event
import gra_afch
import retro
import watchdog

class Retro:
    """the retro module
    """

    VERSION = '0.0.3'

    _conf_dict = None
    event = None
    _clock = None
    _send_json = None
    
    # modules
    event = None
    gra_afch = None
    watchdog = None

    def config(self, module):
        if 'event' == module:
            return self.event.config()
        elif 'gra-afch' == module:
            return self.gra_afch.config()
        elif 'retro' == module:
            return self._conf.json
        elif 'watchdog' == module:
            return self.watchdog.config()
        else:
            assert False

    def path(self, path, file_name):
        return os.path.join(os.path.abspath(os.path.dirname(path)), file_name)

    def events(self, module_name):
        """find module event configuration
        """

        return next((x for x in self._conf_dict['events']
                     if module_name in x), None)

    def find_rotor(self, rotor_name):
        """find rotor
        """

        return next((x for x in self._conf_dict['rotors']
                     if rotor_name in x), None)

    def rotors(self):
        """find rotor definitions
        """

        return self._conf_dict['rotors']

    def template(self):
        return {
                'host': socket.gethostname(),
                'modules': [ 'event',
                             'gra-afch',
                             'retro',
                             'watchdog'
                ],
                'versions': { 'event': self.event.VERSION,
                              'gra-afch': self.gra_afch.VERSION,
                              'retro': self.VERSION,
                              'watchdog': self.watchdog.VERSION
                },
                'configs': { 'event': self.config('event'),
                             'gra_afch': self.config('gra-afch'),
                             'retro': self._conf_dict,
                             'watchdog': self.config('watchdog')
                },
                'date': datetime.now().strftime('%B %d, %Y %H:%M:%S ')
                        + time.localtime().tm_zone,
                'serial': '0000001'
        }

    def exec_(self, op):
        """retro execs
        """

        print('retro.exec_')
        print(op)

    def recv_json(self, obj):
        if 'webapp' in obj:
            webapp = obj['webapp']
            if 'toggle' in webapp:
                self.event.make_event('gra-afch', 'event', 'toggle')

    def send_json(self, id_, value):
        def _message(id_, value):
            fmt = '{{ "id": "{}", "value": "{}" }}'
            return fmt.format(id_, value)

        # print(_message(id_, value))
        self._send_json(json.loads(_message(id_, value)))
    
    def __init__(self, send_json):
        def event_proc():
            while True:
                ev = self.event.find_event('retro')
                self.exec_(ev['retro'])

        self._send_json = send_json

        self._conf_dict = []
        with open(self.path(__file__, '../conf.json'), 'r') as file:
            self._conf_dict = json.load(file)

        # register modules
        self.event = event.Event(self)
        self.gra_afch = gra_afch.GraAfch(self)
        self.watchdog = watchdog.Watchdog(self)

        self.event.register('retro', event_proc)

        def time_proc():
            def timer_():
                thread_ = None
                self.send_json('version', datetime.now().strftime('%B %d, %Y %H:%M:%S'))
                thread_ = Timer(1, timer_)
                thread_.start()

            thread_ = Timer(1, timer_)
            thread_.start()

        self._clock = Thread(target = time_proc)
        self._clock.start()
