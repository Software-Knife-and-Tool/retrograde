#
#
#
.PHONY: install release clean
SHELL=/bin/bash

SYSTEMD = /usr/lib/systemd/system

DEST    = /opt
DIST    = retrograde
APP     = ..

SRCDIRS = \
	modules/event		\
	modules/gra_afch	\
	modules/watchdog	\
	retro			\
	static/css		\
	static/icons		\
        static/icons/favicon_io \
	static/js		\
	templates

PACKAGES = wiringpi flask flask-socketio eventlet dbus-python
help:
	@echo release - package release
	@echo clean

release:
	@install -d $(DIST)
	@install -d $(DIST)/retro

	@install -m 755 ./run.sh $(DIST)/retro
	@install -m 644 $(APP)/app.py $(DIST)/retro	
	@install -m 644 $(APP)/conf.json $(DIST)/retro
	@for i in $(SRCDIRS); do	\
	  install -d $(DIST)/retro/$$i;	\
	  install -m 644 $(APP)/$$i/* $(DIST)/retro/$$i;	\
	done

	@virtualenv $(DIST)/venv

	@(source $(DIST)/venv/bin/activate ; pip3 --quiet install $(PACKAGES))

	@tar cfz $(DIST)-0.0.1.tgz $(DIST)
	@rm -rf $(DIST)

clean:
	@rm -rf $(DIST) $(DIST)-0.0.1.tgz

install:
	@cat $(DIST)-0.0.1.tgz | (cd $(DEST) ; sudo tar xfz -)
	@sudo cp ./retrograde.service $(SYSTEMD)
	@systemctl --system list-unit-files | grep retrograde

clobber: clean
	@sudo rm -rf $(SYSTEMD)/retrograde.service $(DEST)/retrograde
	#@systemctl --system list-unit-files | grep retrograde
