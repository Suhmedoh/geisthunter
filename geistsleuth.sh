#!/bin/bash

# quick and dirty script to set up monitor mode

# run with sudo


# get wifi interface name; mine has ralink in the chipset, change yours accordingly

wifi_interface=$(sudo airmon-ng | grep -i ralink | awk '{print $2}')

# set the interface to monitoring mode

sudo ifconfig ${wifi_interface} down
sudo iwconfig ${wifi_interface} mode monitor
sudo ifconfig ${wifi_interface} up

# open airodump-ng, monitor for 30 seconds, then  parse output
sudo airodump-ng -w victims --output-format csv ${wifi_interface} --write-interval 15

# get a list of networks sorted by most powerful first
# sort -t, -r -n -k9 victims-01.csv | grep -i wpa | sed -n '/, ,\s*$/!p'
