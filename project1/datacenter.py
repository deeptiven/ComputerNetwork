#!/usr/bin/python
# CS6250 Computer Networks Project 1
# Creates a datacenter topology based on command line parameters and starts the Mininet Command Line Interface.

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, output, setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
import argparse
import sys
import os

# Parse Command Line Arguments
parser = argparse.ArgumentParser(description="Datacenter Topologies")

parser.add_argument('--fi',
                    type=int,
                    help=("Number of Fan-in Switches to create."
                    "Must be >= 1"),
                    required=True)

parser.add_argument('--n',
                    type=int,
                    help=("Number of hosts to create in each lower level switch."
                    "Must be >= 1"),
                    required=True)

args = parser.parse_args()

lg.setLogLevel('info')

# Topology to be instantiated in Mininet
class DataCenter(Topo):
    "DataCenter Topology"

    def __init__(self, n=1, delay='0ms', fi=1,  cpu=.01, max_queue_size=None, **params):
        """Star Topology with fi fan-in  zones.
           n: number of hosts per low level switch
           cpu: system fraction for each host
           bw: link bandwidth in Mb/s
           delay: link latency (e.g. 10ms)"""
        self.cpu = 1 / ((n * fi * fi) * 1.5)

        # Initialize topo
        Topo.__init__(self, **params)

        hostConfig = {'cpu': cpu}
        #NOTE:  Switch to Switch links will be bw=10 delay=0
        #NOTE:  Hosts to Switch links will be bw=1 delay=1
        #NOTE:  Use the following configurations as appropriate when creating the links
        swlinkConfig = {'bw': 10, 'delay': '0ms', 'max_queue_size': max_queue_size}
        hostlinkConfig = {'bw': 1, 'delay': '1ms','max_queue_size': max_queue_size}
        tls = self.addSwitch('tls1')
        #TODO: Create your DataCenter Mininet Topology here!
        #NOTE: Top Level Switch is labled tls1 and is created for you
        #NOTE: You MUST label mid level switches as mls1, mls2, ... mlsfi
        #NOTE: You MUST label low level switches s1x1, s1x2...s1xfi... sfix1, sfix2,... sfixfi
        #NOTE: You MUST label hosts as h1x1x1, h1x1x2, ... hfixfixn
        #HINT: Use a loop to construct the topology in pieces. Don't forget the link configuration.

        mls_n = dict()
        for i in range(1, n+1):
            mls["mls" + str(i)]  = self.addSwitch("msl" + str(i))
        #mls1 = self.addSwitch('msl1')
        #mls2 = self.addSwitch('msl2')

        s_fi_x_n = dict()
        for i in range(1, fi+1):
            for j in range(1, n+1):
                switch_name = "s{0}x{1}".format(i, j)
                s_fi_x_n[switch_name] = self.addSwitch(switch_name)


        # s1x1 = self.addSwitch('s1x1')
        # s1x2 = self.addSwitch('s1x2')
        # s2x1 = self.addSwitch('s2x1')
        # s2x2 = self.addSwitch('s2x2')

        h_fi_x_fi_x_n = dict()
        for i in range(1, fi + 1):
            for j in range(1, fi + 1):
                for k in range(1, n + 1)
                host_name = "h{0}x{1}x{2}".format(i, j, k)
                h_fi_x_fi_x_n[host_name] = self.addHost(host_name, **hostConfig)

        # h1x1x1 = self.addHost('h1x1x1', **hostConfig)
        # h1x1x2 = self.addHost('h1x1x2', **hostConfig)
        # h1x1x3 = self.addHost('h1x1x3', **hostConfig)
        # h1x1x4 = self.addHost('h1x1x4', **hostConfig)
        # h1x1x5 = self.addHost('h1x1x5', **hostConfig)

        # h1x2x1 = self.addHost('h1x2x1', **hostConfig)
        # h1x2x2 = self.addHost('h1x2x2', **hostConfig)
        # h1x2x3 = self.addHost('h1x2x3', **hostConfig)
        # h1x2x4 = self.addHost('h1x2x4', **hostConfig)
        # h1x2x5 = self.addHost('h1x2x5', **hostConfig)

        # h2x1x1 = self.addHost('h2x1x1', **hostConfig)
        # h2x1x2 = self.addHost('h2x1x2', **hostConfig)
        # h2x1x3 = self.addHost('h2x1x3', **hostConfig)
        # h2x1x4 = self.addHost('h2x1x4', **hostConfig)
        # h2x1x5 = self.addHost('h2x1x5', **hostConfig)

        # h2x2x1 = self.addHost('h2x2x1', **hostConfig)
        # h2x2x2 = self.addHost('h2x2x2', **hostConfig)
        # h2x2x3 = self.addHost('h2x2x3', **hostConfig)
        # h2x2x4 = self.addHost('h2x2x4', **hostConfig)
        # h2x2x5 = self.addHost('h2x2x5', **hostConfig)

        for mls in mls_n.values():
            self.addLink(tls, mls, **swlinkConfig)
        # self.addLink(tsl, mls1, **swlinkConfig)
        # self.addLink(tsl, mls2, **swlinkConfig)

        for mls in mls_n.values():
            for s in s_fi_x_n.values():
                self.addLink(mls, s, **swlinkConfig)
        # self.addLink(mls1, s1x1, **swlinkConfig)
        # self.addLink(mls1, s1x2, **swlinkConfig)

        # self.addLink(mls2, s2x1, **swlinkConfig)
        # self.addLink(mls2, s2x2, **swlinkConfig)

        for s in s_fi_x_n.values():
            for h in h_fi_x_fi_x_n.values():
                self.addLink(s, h, **hostlinkConfig)

        # self.addLink(s1x1, h1x1x1, **hostlinkConfig)
        # self.addLink(s1x1, h1x1x2, **hostlinkConfig)
        # self.addLink(s1x1, h1x1x3, **hostlinkConfig)
        # self.addLink(s1x1, h1x1x4, **hostlinkConfig)
        # self.addLink(s1x1, h1x1x5, **hostlinkConfig)

        # self.addLink(s1x2, h1x2x1, **hostlinkConfig)
        # self.addLink(s1x2, h1x2x2, **hostlinkConfig)
        # self.addLink(s1x2, h1x2x3, **hostlinkConfig)
        # self.addLink(s1x2, h1x2x4, **hostlinkConfig)
        # self.addLink(s1x2, h1x2x5, **hostlinkConfig)

        # self.addLink(s2x1, h2x1x1, **hostlinkConfig)
        # self.addLink(s2x1, h2x1x2, **hostlinkConfig)
        # self.addLink(s2x1, h2x1x3, **hostlinkConfig)
        # self.addLink(s2x1, h2x1x4, **hostlinkConfig)
        # self.addLink(s2x1, h2x1x5, **hostlinkConfig)

        # self.addLink(s2x2, h2x2x1, **hostlinkConfig)
        # self.addLink(s2x2, h2x2x2, **hostlinkConfig)
        # self.addLink(s2x2, h2x2x3, **hostlinkConfig)
        # self.addLink(s2x2, h2x2x4, **hostlinkConfig)
        # self.addLink(s2x2, h2x2x5, **hostlinkConfig)

def main():
    "Create specified topology and launch the command line interface"
    topo = DataCenter(n=args.n, fi=args.fi)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
