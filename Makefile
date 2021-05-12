#
#
#
.PHONY: clean

clean:
	@rm -rf instance __pycache__

venv:
	@virtualenv venv

install:
	@pip install virtualenv flask uWSGI flask-socketio eventlet pylint

uwsgi:
	@uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file app.py --callable app
