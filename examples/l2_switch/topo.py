#!/usr/bin/python

# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep
import os
import subprocess

_THIS_DIR = os.path.dirname(os.path.realpath(__file__))

class MyTopo(Topo):
    def __init__(self, args, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        s1 = self.addSwitch('s1',
                      sw_path = args.behavioral_exe,
                      json_path = args.json,
                      thrift_port = args.base_port,
                      pcap_dump = False,
                      device_id = 1)

        for i in range(args.num_host):
            h = self.addHost('h%d' % (i+1))
            self.addLink(h, s1, params1={'ip': '10.0.0.%d/8' % (i+1)})


def main(args):
    topo = MyTopo(args)

    net = Mininet(topo = topo,
                  host = P4Host,
                  switch = P4Switch,
                  autoSetMacs = True,
                  controller = None)

    net.start()

    for n in range(args.num_host): 
        h = net.get('h%d' % (n+1))
        for off in ["rx", "tx", "sg"]:
            cmd = "/sbin/ethtool --offload eth0 %s off" % off
            h.cmd(cmd)
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
        h.cmd("iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP")
        #h.cmd("route add -net 224.0.0.0 netmask 224.0.0.0 eth0")

    sleep(1)

    cmd = [args.cli, args.json, str(args.base_port)]
    with open("commands.txt", "r") as f:
        print " ".join(cmd)
        try:
            output = subprocess.check_output(cmd, stdin = f)
            print output
        except subprocess.CalledProcessError as e:
            print e
            print e.output


    print "Ready !"

    CLI( net )
    net.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mininet demo')
    parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                        type=str, action="store", required=True)
    parser.add_argument('--json', help='Path to P4 program',
                        type=str, action="store", required=True)
    parser.add_argument('--cli', help='Path to BM CLI',
                        type=str, action="store", required=True)
    parser.add_argument('--base-port', help='Thrift base port',
                        type=int, action="store", default=22222)
    parser.add_argument('--num-host', help='Number of hosts',
                        type=int, action="store", default=4)
    args = parser.parse_args()
    setLogLevel( 'info' )
    main(args)
