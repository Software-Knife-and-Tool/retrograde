#
#
#
.PHONY: clean

clean:
	@rm -rf instance __pycache__

venv:
	@virtualenv venv

install:
	@sudo apt-get install bluetooth bluez libbluetooth-dev
	@pip3 install wiringpi flask uWSGI flask-socketio eventlet pylint pybluez bluedot dbus-python
