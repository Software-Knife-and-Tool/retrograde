#
#
#
.PHONY: lint venv
SRCS = \
	app.py         			\
	module				\
	modules/event/*.py		\
	modules/gra_afch/*.py		\
	modules/retro/*.py		\
	modules/watchdog/*.py

BASE = /home/putnamjm/retrograde/retrograde

BIN = $(BASE)/venv/bin
PACKAGES = $(BASE):$(BASE)/modules:$(BASE)/venv/lib/python3.7/site-packages

venv:
	@virtualenv venv

install:
	@sudo apt-get install bluetooth bluez libbluetooth-dev
	@pip3 install wiringpi flask uWSGI flask-socketio eventlet pylint pybluez bluedot dbus-python

blank:
	@sudo env "PATH=$(BIN)" "PYTHONPATH=$(PACKAGES)" python3 modules/gra_afch/blank.py

run:
	@sudo env "PATH=$(BIN)" "PYTHONPATH=$(PACKAGES)" python3 app.py

profile:
	@sudo env "PATH=$(BIN)" "PYTHONPATH=$(PACKAGES)" python3 -m cProfile -s cumtime gra_afch/blank.py

uwsgi:
	@uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file app.py --callable app

lint:

	@for i in $(SRCS); do		\
	    echo -n $$i ": ";		\
	    env "PATH=$(BIN)" "PYTHONPATH=$(PYTHONPATH):$(PACKAGES)" pylint $$i | egrep -v "^-";	\
	done

lint-summary:
	@make lint | grep code
