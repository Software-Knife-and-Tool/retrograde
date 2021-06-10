#
#
#

.PHONY: lint venv
SRCS = \
	app.py         		\
	config/*.py

BASE = /home/putnamjm/retrograde/config

BIN = $(BASE)/venv/bin
PACKAGES = $(BASE):$(BASE)/venv/lib/python3.7/site-packages

venv:
	@virtualenv venv

install:
	# @sudo apt-get install hostapd
	# @sudo systemctl unmask hostapd
	# @sudo systemctl enable hostapd

	# sudo nano /etc/dhcpcd.conf
	# interface wlan0
	#    static ip_address=192.168.4.1/24
	#    nohook wpa_supplicant

	# sudo nano /etc/hostapd/hostapd.conf
	# country_code=US
	# interface=wlan0
	# ssid=retrograde
	# hw_mode=g
	# channel=7
	# macaddr_acl=0
	# auth_algs=1
	# ignore_broadcast_ssid=0
	# wpa=2
	# wpa_passphrase=retrograde
	# wpa_key_mgmt=WPA-PSK
	# wpa_pairwise=TKIP
	# rsn_pairwise=CCMP

	@pip3 install flask uWSGI flask-socketio eventlet pylint dbus-python

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
