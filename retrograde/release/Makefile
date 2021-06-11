#
#
#
.PHONY: install release clean
SHELL=/bin/bash

SYSTEMD = /usr/lib/systemd/system

DIST    = /opt
DEST    = retrograde
APP     = ..

SRCDIRS = \
	modules/event		\
	modules/gra_afch	\
	modules/watchdog	\
	retro			\
	static/css		\
	static/icons		\
	static/js		\
	templates

PACKAGES = wiringpi flask flask-socketio eventlet dbus-python
help:
	@echo release - package release
	@echo clean

release:
	@install -d $(DEST)
	@install -d $(DEST)/retro

	@install -m 755 ./run.sh $(DEST)/retro
	@install -m 644 $(APP)/app.py $(DEST)/retro	
	@install -m 644 $(APP)/conf.json $(DEST)/retro
	@for i in $(SRCDIRS); do	\
	  install -d $(DEST)/retro/$$i;	\
	  install -m 644 $(APP)/$$i/* $(DEST)/retro/$$i;	\
	done

	@virtualenv $(DEST)/venv

	@(source $(DEST)/venv/bin/activate ; pip3 --quiet install $(PACKAGES))

	@tar cfz $(DEST)-0.0.1.tgz $(DEST)
	@rm -rf $(DEST)

clean:
	@rm -rf $(DEST) $(DEST)-0.0.1.tgz

install:
	@cat $(DEST)-0.0.1.tgz | (cd $(DIST) ; sudo tar xfz -)
	@sudo cp ./retrograde.service $(SYSTEMD)
	@systemctl --system list-unit-files | grep retrograde

clobber: clean
	@sudo rm -rf $(SYSTEMD)/retrograde.service $(DIST)/retrograde
	@systemctl --system list-unit-files | grep retrograde
