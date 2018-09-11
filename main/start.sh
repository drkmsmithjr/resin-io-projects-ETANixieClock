#!/usr/bin/bash

#start wifi-connect.  This will start an access point if none is found
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

#Is there an active WiFi connection?
iwgetid -r

if [ $? -eq 0 ]; then
    printf 'Skipping WiFi Connect\n'
else
    printf 'Starting WiFi Connect\n'
    ./wifi-connect --portal-ssid="ETANixieClock Connect" --activity-timeout=300
fi

# Default to UTC if no TIMEZONE env variable is set
echo "Setting time zone to ${TIMEZONE=America/Los_Angeles}"
# This only works on Debian-based images
echo "${TIMEZONE}" > /etc/timezone
dpkg-reconfigure tzdata

# GoogleKey will be passed from Resin
python /app/ETAclock.py ${GOOGLEKEY}


