import os
import socket
import lumen
import time

from datetime import date, datetime
from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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

    return app
