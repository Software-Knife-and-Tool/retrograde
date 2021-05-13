#
# ntag2 release install
#
install -d /opt/ntag2
install -d /opt/ntag2/ntag2
install -m 755 ./__init__.py /opt/ntag2/ntag2
install -m 755 ./ntag2-daemon.conf /opt/ntag2
install -m 755 ./ntag2-tool /opt/ntag2
install -m 755 ./ntag2-daemon /opt/ntag2
# install -m 755 ./ntag2.service /etc/systemd/system
# systemctl daemon-reload
# systemctl start ntag2
