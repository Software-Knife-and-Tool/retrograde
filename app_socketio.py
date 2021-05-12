import os
import socket
import lumen
import time

from datetime import date, datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    # SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

conf_dict = lumen.lumen()

# render_template('index.html',
#                host=socket.gethostname(),
#                version=lumen.version(),
#                serial='0001',
#                conf_dict=conf_dict,
#                date=datetime.now().strftime('%B %d, %Y %H:%M:%S ')
#                + time.localtime().tm_zone,
#                )

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
    conf_dict = lumen.lumen()
    return render_template('index.html',
                           host=socket.gethostname(),
                           version=lumen.version(),
                           serial='0001',
                           conf_dict=conf_dict,
                           date=datetime.now().strftime('%B %d, %Y %H:%M:%S ')
                           + time.localtime().tm_zone,
                           )

socketio.run(app)
