#!/usr/bin/env python3
'''
    License: do-whatever-you-want-dont-blame-me

    https://github.com/gcmartinelli/probe-sniffer


    Records 802.11 probe requests from devices
    (i.e. what WIFI networks are the devices around you
    looking for?).


    Requirements:
            Linux
            iwconfig (Linux utility)
            Python 3
            scapy - https://scapy.net

    Usage:
            python listen.py <interface_name> [filename]
            
            If no filename is passed, it will create a dump.txt
            file.

    Detail:
            interface_name can be found using the command

            iwconfig

'''

import threading
import os
import sys
import time
import random
from scapy.all import sniff, Dot11ProbeReq

def channel_hop(iface):
    ''' Changes the network interface channel randomly
        every 500ms '''
    stop = False
    while not stop:
        chan = random.randint(1,14)
        os.system(f"iwconfig {iface} channel {chan}")
        time.sleep(0.5)

def find_probe(packet):
    ''' Parses 802.11 network probes and saves to disk '''
    with open(filename, 'a') as dumpfile:
        if packet.haslayer(Dot11ProbeReq):
            probe = packet.getlayer(Dot11ProbeReq).info.decode()
            if probe not in probe_reg and probe != "":
                probe_reg.append(probe)
                dumpfile.write(f"{probe}\n")
                print(f"Probe found: {probe}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        iface = sys.argv[1]
        filename = "dump.txt"
    elif len(sys.argv) == 3:
        iface = sys.argv[1]
        filename = sys.argv[2]
    else:
        print("usage: listen <interface name> [filename]")
        sys.exit(1)

    if os.path.isfile(filename):
        os.system(f"rm {filename}")

    try:
        thread = threading.Thread(target=channel_hop, args=(iface, ), name="chan_hopper")
        thread.daemon = True
        thread.start()

        probe_reg = []
        sniff(iface=iface, prn=find_probe)

    except Exception as e:
        print(f"[*] Error: {e}")
        sys.exit(1)
