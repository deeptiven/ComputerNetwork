#!/usr/bin/python
# CS 6250 Spring 2020 - Project 6 - SDN Firewall
# build argyle-v12

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet


def make_firewall_policy(config):
    # You may place any user-defined functions in this space.
    # You are not required to use this space - it is available if needed.

    # feel free to remove the following "print config" line once you no longer need it
    # it will not affect the performance of the autograder
    # print config

    # The rules list contains all of the individual rule entries.

    rules = []

    for entry in config:

        # TODO - This is where you build your firewall rules...
        # Note that you will need to delete the rule line below when you create your own
        # firewall rules.  Refer to the Pyretic github documentation for instructions on how to
        # format these commands.
        # Example (but incomplete)
        # rule = match(srcport = int(entry['port_src']))
        # The line below is hardcoded to match TCP Port 1080.  You must remove this line
        # in your completed assignments.  Do not hardcode your solution - you must use items
        # in the entry[] dictionary object to build your final ruleset for each line in the
        # policy file.

        # Delete this line when you build your implementation.
        # rule = match(dstport=1080, ethtype=packet.IPV4, protocol=packet.TCP_PROTO)

        tcp_rule, udp_rule, icmp_rule, other_rule, rule = None, None, None, None, None

    # print entry

        if (entry['macaddr_src'] == '-' and entry['macaddr_dst'] == '-' and entry['ipaddr_src'] == '-' and entry[
            'ipaddr_dst'] == '-' and entry['port_src'] == '-' and entry['port_dst'] == '-' and entry['protocol'] == '-' and
                entry['ipproto'] == '-'):
            print "Allow everything"
        else:
            # MAC address
            if (entry['macaddr_src'] != '-') and (entry['macaddr_dst'] != '-'):
                rule = match(srcmac=EthAddr(entry['macaddr_src']), dstmac=EthAddr(entry['macaddr_dst']))
            elif entry['macaddr_src'] != '-':
                rule = match(srcmac=EthAddr(entry['macaddr_src']))
            elif entry['macaddr_dst'] != '-':
                rule = match(dstmac=EthAddr(entry['macaddr_dst']))

            # IP address
            ip_rule = None
            if (entry['ipaddr_src'] != '-') and (entry['ipaddr_dst'] != '-'):
                ip_rule = match(srcip=IPAddr(entry['ipaddr_src']), dstip=IPAddr(entry['ipaddr_dst']))
            elif entry['ipaddr_src'] != '-':
                ip_rule = match(srcip=IPAddr(entry['ipaddr_src']))
            elif entry['ipaddr_dst'] != '-':
                ip_rule = match(dstip=IPAddr(entry['ipaddr_dst']))

            if ip_rule:
                rule = rule & ip_rule if rule else ip_rule

            # Source & Destination ports
            port_rule = None
            if entry['port_src'] != '-':
                port_rule = match(srcport=int(entry['port_src']))
            if entry['port_dst'] != '-':
                port_rule = match(dstport=int(entry['port_dst']))

            if port_rule:
                rule = rule & port_rule if rule else port_rule

            # Process protocol
            if entry['protocol'] == 'T':    # TCP
                tcp_rule = match(ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
                tcp_rule = rule & tcp_rule if rule else tcp_rule
                rules.append(tcp_rule)
            elif entry['protocol'] == 'U':  # UDP
                udp_rule = match(ethtype=packet.IPV4, protocol=packet.UDP_PROTO)
                udp_rule = rule & udp_rule if rule else udp_rule
                rules.append(udp_rule)
            elif entry['protocol'] == 'I':  # ICMP
                icmp_rule = match(ethtype=packet.IPV4, protocol=packet.ICMP_PROTO)
                icmp_rule = rule & icmp_rule if rule else icmp_rule
                rules.append(icmp_rule)
            elif entry['protocol'] == 'B':  # TCP and UDP
                tcp_rule = match(ethtype=packet.IPV4, protocol=packet.TCP_PROTO)
                tcp_rule = rule & tcp_rule if rule else tcp_rule
                rules.append(tcp_rule)

                udp_rule = match(ethtype=packet.IPV4, protocol=packet.UDP_PROTO)
                udp_rule = rule & udp_rule if rule else udp_rule
                rules.append(udp_rule)
            elif entry['protocol'] == 'O':  # Other protocols
                ipnum = int(entry['ipproto'])
                other_rule = match(ethtype=packet.IPV4, protocol=ipnum)
                other_rule = rule & other_rule if rule else other_rule
                rules.append(other_rule)
            else:
                rules.append(rule)

    allowed = ~(union(rules))

    return allowed
