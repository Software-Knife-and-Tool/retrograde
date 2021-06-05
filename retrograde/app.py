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

import socket
import time
import json

from flask import Flask, render_template
from flask_socketio import SocketIO

from module import Module

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

VERSION = '0.0.1'
_module = Module()

socketio = SocketIO(app)

@socketio.on('json')
def recv_message(json_):
    print('server:receive json:')
    print(json.loads(json_))

@socketio.on('json')
def send_message(obj):
    print('server:send json: ')
    print(obj)
    socketio.send('json', json.dumps(obj))

@app.route('/')
def render():
    return render_template('index.html',
                           version = VERSION,
                           template = _module.retro.template(_module))

socketio.run(app, host='0.0.0.0')
# send_message({'date': datetime.now().strftime('%B %d, %Y %H:%M:%S ')
#              + time.localtime().tm_zone})
