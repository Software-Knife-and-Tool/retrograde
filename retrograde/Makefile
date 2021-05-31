#
#
#
.PHONY: lint venv
SRCS = \
	app.py     	        \
	event/__init__.py	\
	gra_afch/blank.py	\
	gra_afch/__init__.py	\
	gra_afch/ncs31x.py	\
	retro/config.py		\
	retro/__init__.py

PYTHONBIN = /home/lumino/retrograde/retrograde/venv/bin
PYTHONPATH = /home/lumino/retrograde/retrograde/gra_afch:/home/lumino/retrograde/retrograde/retro:/home/lumino/retrograde/retrograde/venv/lib/python3.7/site-packages

venv:
	@virtualenv venv

install:
	@sudo apt-get install bluetooth bluez libbluetooth-dev
	@pip3 install wiringpi flask uWSGI flask-socketio eventlet pylint pybluez bluedot dbus-python

blank:
	@sudo env "PATH=$(PYTHONBIN):$(PATH)" "PYTHONPATH=$(PYTHONPATH)" python3 gra_afch/blank.py

run:
	@sudo env "PATH=$(PYTHONBIN):$(PATH)" "PYTHONPATH=$(PYTHONPATH)" python3 app.py

profile:
	@sudo env "PATH=$(PYTHONBIN):$(PATH)" "PYTHONPATH=$(PYTHONPATH)" python3 -m cProfile -s cumtime gra_afch/blank.py

uwsgi:
	@uwsgi --http :5000 --gevent 1000 --http-websockets --master --wsgi-file app.py --callable app

lint:
	@for i in $(SRCS); do		\
	    echo -n $$i ": ";		\
	    pylint $$i | egrep -v "^-";	\
	done

lint-summary:
	@make lint | grep code
