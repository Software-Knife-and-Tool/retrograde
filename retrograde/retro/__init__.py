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

"""retro manages modules and webapp events

Classes:
    Retro

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

Misc variables:

    VERSION

"""

import json
import os
import socket
import sys
import time

from datetime import datetime

from flask_socketio import SocketIO
from threading import Thread, Lock, Timer

import console
import event
import gra_afch
import watchdog

class Retro:
    """the retro module
    """

    VERSION = '0.0.3'

    # modules
    console = None
    event = None
    gra_afch = None
    watchdog = None
    retro = None

    _conf_dict = None
    _send_json = None

    def path(self, path, file_name):
        """make an absolute path to module
        """

        return os.path.join(os.path.abspath(os.path.dirname(path)), file_name)

    def host_config(self):
        """if the host config file doesn't exist, create one
        """


    def config(self, module):
        """get the config dict from the named module
        """

        conf_ = None

        if 'console' == module:
            conf_ = self.console.config()
        elif 'event' == module:
            conf_ = self.event.config()
        elif 'gra-afch' == module:
            conf_ = self.gra_afch.config()
        elif 'retro' == module:
            conf_ =  self._conf.json
        elif 'watchdog' == module:
            conf_ = self.watchdog.config()
        else:
            assert False

        return conf_

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
        """return webapp state
        """
        return {
                'host': socket.gethostname(),
                'modules': [ 'event',
                             'console',
                             'gra-afch',
                             'retro',
                             'watchdog'
                ],
                'versions': { 'event': self.event.VERSION,
                              'console': self.console.VERSION,
                              'gra-afch': self.gra_afch.VERSION,
                              'retro': self.VERSION,
                              'watchdog': self.watchdog.VERSION,
                },
                'configs': { 'event': self.config('event'),
                             'console': self.config('console'),
                             'gra_afch': self.config('gra-afch'),
                             'retro': self._conf_dict,
                             'watchdog': self.config('watchdog')
                },
                'wap': 'not configured',
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
        """get an event from the webapp
        """
        if 'webapp' in obj:
            webapp = obj['webapp']
            if 'toggle-button' in webapp:
                self.event.make_event('gra-afch', 'event', 'toggle')
            elif 'soft-reset' in webapp:
                print('soft- reset')
            elif 'hard-reset' in webapp:
                print('hard- reset')
            else:
                assert False
                
    def send_json(self, id_, value):
        """format a message and send it to the webapp
        """
        def _message(id_, value):
            fmt = '{{ "id": "{}", "value": "{}" }}'
            return fmt.format(id_, value)

        # print(_message(id_, value))
        self._send_json(json.loads(_message(id_, value)))

    def __init__(self, send_json):
        """create Retro class
        """
        def event_proc():
            while True:
                ev = self.event.find_event('retro')
                self.exec_(ev['retro'])

        self._send_json = send_json

        # static configuration
        self._conf_dict = []
        with open(self.path(__file__, '../conf.json'), 'r') as file:
            self._conf_dict = json.load(file)

        host_dict_ = []
        host_config_path_ = self.path(__file__, './host.json')

        if os.path.exists(host_config_path_):
            with open(host_config_path_, 'r') as file:
                host_dict_ = json.load(file)

        # add this stuff to _config_dict somehow

        self.event = event.Event(self)
        self.console = console.Console(self)
        self.gra_afch = gra_afch.GraAfch(self)
        self.watchdog = watchdog.Watchdog(self)

        self.event.register('retro', event_proc)
