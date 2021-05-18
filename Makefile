#
#
#
.PHONY: clean

clean:
	@rm -rf instance __pycache__

venv:
	@virtualenv venv

install:
	@pip3 install virtualenv flask uWSGI flask-socketio eventlet pylint

lint:
	make -C lumino lint

uwsgi:
	@uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file app.py --callable app
