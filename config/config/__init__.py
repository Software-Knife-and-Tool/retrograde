##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## config initialization
##
###########

"""config manages modules webapp events

Classes:
    Config

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

# from flask_socketio import SocketIO

class Config:
    """the retro module
    """

    VERSION = '0.0.3'

    _conf_dict = None
    _send_json = None

    def path(self, path, file_name):
        """make an absolute path to module
        """

        return os.path.join(os.path.abspath(os.path.dirname(path)), file_name)

    def config(self, module):
        """get the config dict from the named module
        """

        conf_ = None
        if 'event' == module:
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

    def template(self):
        """return webapp state
        """

        return {
                'host': socket.gethostname(),
                'date': datetime.now().strftime('%B %d, %Y %H:%M:%S ')
                        + time.localtime().tm_zone,
                'serial': '0000001'
        }

    def recv_json(self, obj):
        """get an event from the webapp
        """

        if 'webapp' in obj:
            webapp = obj['webapp']
            print(webapp)

    def send_json(self, id_, value):
        """format a message and send it to the webapp
        """

        def _message(id_, value):
            fmt = '{{ "id": "{}", "value": "{}" }}'
            return fmt.format(id_, value)

        # print(_message(id_, value))
        self._send_json(json.loads(_message(id_, value)))

    def __init__(self, send_json):
        """create Config class
        """
        self._send_json = send_json

        # static configuration
        self._conf_dict = []
        with open(self.path(__file__, './conf.json'), 'r') as file:
            self._conf_dict = json.load(file)
