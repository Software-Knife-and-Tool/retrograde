#
#
#
.PHONY: clean

clean:
	@rm -rf instance __pycache__

venv:
	@virtualenv venv

install:
	@pip3 install wiringpi flask uWSGI flask-socketio eventlet pylint
