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

    App: retrograde entry point

"""

import socket
import time
import json

from datetime import datetime

from flask import Flask, render_template
from flask_socketio import SocketIO

import retro

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

_retrograde_conf = retro.retro()

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
                           host = socket.gethostname(),
                           version = retro.VERSION,
                           serial = '0000001',
                           retrograde_conf = _retrograde_conf,
                           gra_afch_conf = _retrograde_conf,
                           skew = 0.0,
                           date = datetime.now().strftime('%B %d, %Y %H:%M:%S ')
                           + time.localtime().tm_zone,
                           )

socketio.run(app, host='0.0.0.0')
# send_message({'date': datetime.now().strftime('%B %d, %Y %H:%M:%S ')
#              + time.localtime().tm_zone})
