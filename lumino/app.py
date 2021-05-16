##########
##
##  SPDX-License-Identifier: MIT
##
##  Copyright (c) 2017-2022 James M. Putnam <putnamjm.design@gmail.com>
##
##########

##########
##
## lumino app
##
###########
""" i'm a module docstring """

import socket
import time

from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO

import lumino
import gra_afch

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

_gra_afch_conf = None

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    print('server: received message: ' + data)

@socketio.on('message')
def send_message(data):
    print('server:send message: ' + data)
    socketio.run(app)
    send_message(datetime.now().strftime('%B %d, %Y %H:%M:%S ')
                 + time.localtime().tm_zone)

@app.route('/')
def render():
    return render_template('index.html',
                           host=socket.gethostname(),
                           version=lumino.VERSION,
                           serial='0001',
                           lumino_conf=_lumino_conf,
                           gra_afch_conf=_gra_afch_conf,
                           rotor=lumino.default_rotor(),
                           skew=0.0,
                           date=datetime.now().strftime('%B %d, %Y %H:%M:%S ')
                           + time.localtime().tm_zone,
                           )

# if __name__ == '__main__':
_lumino_conf = lumino.lumino()
_gra_afch_conf = gra_afch.gra_afch()

socketio.run(app, host='0.0.0.0')
#    socketio.run(app, host='0.0.0.0', debug=True)
