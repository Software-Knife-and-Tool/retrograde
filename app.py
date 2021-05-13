import os
import socket
import lumino
# import gra_afch
import time

from datetime import date, datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

_conf_dict = None

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
def init():
    _conf_dict = lumino.lumino()
    return render_template('index.html',
                           host=socket.gethostname(),
                           version=lumino.version(),
                           serial='0001',
                           conf=_conf_dict,                         
                           skew=0.0,
                           wap=_conf_dict['wap'],
                           date=datetime.now().strftime('%B %d, %Y %H:%M:%S ')
                           + time.localtime().tm_zone,
                           )

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
#    socketio.run(app, host='0.0.0.0', debug=True)
