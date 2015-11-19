#!/usr/bin/env python
from scapy.all import *

if __name__=='__main__':
    sniff(iface='eth0', prn = lambda x : hexdump(x))
