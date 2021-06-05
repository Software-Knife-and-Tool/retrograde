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

def _message(id_, value):
    fmt = '{{ "id": "{}", "value": "{}" }}'
    return fmt.format(id_, value)

@socketio.on('json')
def send_json(obj):
    socketio.send(obj, obj)

_retro = Retro(send_json)

@socketio.on('connect')
def _con_message():
    # print('webapp connects: ')
    send_json(json.loads(_message('version', VERSION)))

@socketio.on('disconnect')
def _discon_message():
    pass
    # print('webapp disconnects: ')

@socketio.on('json')
def recv_json(json_):
    pass
    # print('receive json: ', end='')
    # print(str(json_))

@app.route('/')
def render():
    return render_template('index.html',
                           version = VERSION,
                           template = _retro.template())

socketio.run(app, host='0.0.0.0')
