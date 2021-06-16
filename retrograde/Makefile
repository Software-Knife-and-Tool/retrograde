#
#
#
.PHONY: lint venv

SRCS = \
	app.py         		\
	modules/event/*.py	\
	modules/gra_afch/*.py	\
	modules/watchdog/*.py	\
	retro/*.py

BASE = /home/putnamjm/retrograde/retrograde

BIN = $(BASE)/venv/bin
PACKAGES = $(BASE):$(BASE)/modules:$(BASE)/venv/lib/python3.7/site-packages

venv:
	@virtualenv venv

install:
	@pip3 install wiringpi flask uWSGI flask-socketio eventlet pylint dbus-python

blank:
	@sudo env "PATH=$(BIN)" "PYTHONPATH=$(PACKAGES)" python3 modules/gra_afch/blank.py

run:
	@sudo env "PATH=$(BIN)" "PYTHONPATH=$(PACKAGES)" python3 app.py

profile:
	@sudo env "PATH=$(BIN)" "PYTHONPATH=$(PACKAGES)" python3 -m cProfile -s cumtime gra_afch/blank.py

format:
	@yapf -i -vv $(SRCS)

uwsgi:
	@uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file app.py --callable app

lint:
	@for i in $(SRCS); do		\
	    echo -n $$i ": ";		\
	    env "PATH=$(BIN)" "PYTHONPATH=$(PYTHONPATH):$(PACKAGES)" pylint $$i | egrep -v "^-";	\
	done
