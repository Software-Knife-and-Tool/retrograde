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

"""

    App: retrograde entry point and webapp

"""

import json

from flask import Flask, render_template
from flask_socketio import SocketIO

from retro import Retro

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

VERSION = '0.0.2'
socketio = SocketIO(app)

@socketio.on('json')
def send_json(obj):
    # print('send json: ', end='')
    # print(obj)
    socketio.send(obj, obj)

@socketio.on('connect')
def _con_message():
    def _message(id_, value):
        fmt = '{{ "id": "{}", "value": "{}" }}'
        return fmt.format(id_, value)

    # print('server: webapp connects: ')
    send_json(json.loads(_message('version', VERSION)))

_retro = Retro(send_json)

@socketio.on('disconnect')
def _discon_message():
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
