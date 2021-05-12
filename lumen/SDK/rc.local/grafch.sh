#! /bin/bash
HOSTNAME=thuria
AP=AP
PASSWD=PASSWD

# set hostname
hostnamectl set-hostname $HOSTNAME
sed -e "1,$$s/raspberrypi/$HOSTNAME/g" /etc/hosts | tee /etc/hosts > /dev/null
# change pi password
chpasswd <<<"pi:thuria"
# create thuria user
adduser --disabled-password --gecos "" thuria
usermod -aG sudo thuria
chpasswd <<<"thuria:thuria"
# enable ssh
systemctl enable ssh
systemctl start ssh
# configure wifi
cat <<EOF >> /etc/wpa_supplicant/wpa_supplicant.conf
network={
    ssid="$AP"
    psk="$PASSWD"
}
country=US
EOF
wpa_cli -i wlan0 reconfigure
rfkill unblock 0
ifconfig wlan0 up
until ip -h link show | grep wlan0 | grep " UP" > /dev/null 2>&1
do
    echo -n "."
    sleep 2
done
until ping -c 1 raspberrypi.org > /dev/null &>21
do
    echo -n "."
    sleep 2
done

# update everything
apt-get update -y
apt-get upgrade -y
# install git
apt-get install git -y
# install wiringpi
apt-get install wiringpi -y
# configure SPI
echo "dtparam=spi-on" >> /boot/config.txt

# clean up
rm /etc/rc.local
touch /etc/rc.local
chmod 755 /etc/rc.local

# reboot for SPI changes
reboot
