This readme is a work in progress.
v0.0.1
# SPOOKYZEITGEIST  
  
## GEISTHUNTER  
  
It's a python script that listens on an open port for hashes, attempts to crack them, and then sends the hash back out to a predefined system  
  
## GEISTSLEUTH  
  
It's a shell script that sets a wifi interface into monitoring mode, attempts to grab the PMKID from the network with the strongest signal, and sends it to a predefines system  
  
## HOW DO THEY WORK TOGETHER  
  
If you want to crack a wifi password, you'll want computing power in order to bruteforce or run a wordlist quickly against it.  
If you want to get on said wifi network, you'll need to be close enough to it. 
Powerful computers are generally big, power hungry, and not stealthy. Your gaming pc probably isn't a good candidate to hack the wifi at Starbucks because it'd be pretty weird for you to lug it in there and set it up.  
On the other hand, a raspberry pi with a usb wifi adapter and battery pack can fit inside a backpack or a purse quite easily, but lacks the power to efficiently crack passwords.  
  
This is where the geistsuite comes in; you plug a usb wifi adapter(that can be set to monitoring mode) into your pi, connect a battery pack/portable charger to it, set it to auto connect to your phone's hotspot and have it run geistsleuth on startup. It will attempt to get the info needed to crack the highest power(most likely closest) wifi network, and send that info to a remote machine, such as your gaming pc, or a linux server.  
  
The PC/server will use geisthunter to listen for the info needed to crack the password, and use hashcat to attempt to crack it. If it's successful, it will then send the wifi SSID and password to another machine; This could be back to the raspberry pi, which has a screen and will output the info, or it could post it to your website so you can view it with your phone browser, or save it locally on the machine, so you can ssh in with juiceSSH from your phone and view the info.  
  
## THIS IS A WORK IN PROGRESS  
  
## REQUIREMENTS  
You'll need to set up your raspberrypi to connect to your phone's hostspot if it's available so it can send back the data
https://raspberrypi.stackexchange.com/questions/11631/how-to-setup-multiple-wifi-networks

### HARDWARE  
2 machines, ideally a powerful server for cracking hashes and a raspberry pi
&nbsp;&nbsp;&nbsp;&nbsp;I'm using an old lenovo y580 with an nvidia gtx 660m running linux, and a raspberry pi 3 B+
A usb wifi adapter with monitoring mode
&nbsp;&nbsp;&nbsp;&nbsp;I'm using an Alfa AWUS036NEH I bought on ebay
A battery pack for the raspberry pi
&nbsp;&nbsp;&nbsp;&nbsp;I'm using a PocketJuice Slim Pro 5000mah I had lying around

#### Optional:
A screen for your raspberry pi to see the ssid and password of the cracked wifi
&nbsp;&nbsp;&nbsp;&nbsp;I'm using an Adafruit pioled screen: https://www.adafruit.com/product/3527

### Installation instructions
You'll want to git clone the repo.  The hash cracking server only needs geisthunter, and the wifi hacking device only needs geistsleuth, so you don't need both scripts on both machines.
You'll also need the following:
On the pi(wifi-hacking-device):
https://github.com/ZerBea/hcxtools
https://github.com/ZerBea/hcxdumptool
On the server(hash-cracking-server):
python3
hashcat
