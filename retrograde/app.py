##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## retrograde app
##
###########

"""app: retrograde entry point

    flask/socketio configuration
    webapp socket protocol

See module retro for system interface.

Classes:

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

Misc variables:

    VERSION
    app
    socketio

"""

import os
import json

from flask import Flask, render_template
from flask_socketio import SocketIO

from retro import Retro

VERSION = '0.0.2'

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

try:
    socketio = SocketIO(app)

    @socketio.on('json')
    def send_json(obj):
        # print('send json: ', end='')
        # print(obj)
        socketio.send(obj, obj)

    @socketio.on('connect')
    def _connect():
        def fmt_(id_, value):
            fmt = '{{ "id": "{}", "value": "{}" }}'
            return fmt.format(id_, value)

        # print('server: webapp connects: ')
        send_json(json.loads(fmt_('version', VERSION)))

    _retro = Retro(send_json)

    @socketio.on('disconnect')
    def _disconnect():
        pass
        # print('webapp disconnects: ')

    @socketio.on('json')
    def recv_json(json_):
        # print('receive json: ', end='')
        # print(str(json_))
        _retro.recv_json(json_)

    @app.route('/')
    def render():
        return render_template('index.html',
                               version = VERSION,
                               template = _retro.template())

    socketio.run(app, host='0.0.0.0')

except Exception:
    os.exit(1)

