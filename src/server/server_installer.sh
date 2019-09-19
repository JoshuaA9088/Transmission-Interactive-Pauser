#!/bin/bash

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

# Create user: transmissionpauser
# Home: /opt/transmission_pauser
# Group: transmissionpauser
useradd -m -d /opt/transmission_pauser -s /bin/bash -c "Transmission Pauser User" -U transmissionpauser
addgroup transmissionpauser
usermod -G transmissionpauser transmissionpauser

# Copy essential files to home.
cp server.py /opt/transmission_pauser/.
cp server_settings.ini /opt/transmission_pauser/settings.ini
cp server.service /etc/systemd/system/transmission_pauser.service

# Adjust permissions
chgrp transmissionpauser /opt/transmission_pauser/server.py
chgrp transmissionpauser /opt/transmission_pauser/settings.ini
chgrp transmissionpauser /etc/openvpn/openvpn-status.log
# root:root
chgrp root /etc/systemd/system/transmission_pauser.service
chown root:root /etc/systemd/system/transmission_pauser.service

chmod 640 /opt/transmission_pauser/server.py
chmod 640 /opt/transmission_pauser/settings.ini
chmod 640 /etc/openvpn/openvpn-status.log

systemctl daemon-reload
systemctl start transmission_pauser.service
systemctl enable transmission_pauser.service
systemctl status transmission_pauser.service
