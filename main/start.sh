#!/usr/bin/bash

# run the process loop
python /app/src/process.py

#start resisn-wifi-connect
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
./resin-wifi-connect --clear=false

# Default to UTC if no TIMEZONE env variable is set
echo "Setting time zone to ${TIMEZONE=UTC}"
# This only works on Debian-based images
echo "${TIMEZONE}" > /etc/timezone
dpkg-reconfigure tzdata

# Replace this below with your own application start
# It just idles in this example.
# GoogleKey will be passed from Resin

python /app/ETAclock.py ${GOOGLEKEY}

done
