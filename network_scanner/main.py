#!/usr/bin/env python3

import scapy.all as scapy
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--range", dest="ip_range", help="IP range to query")
    arguments = parser.parse_args()
    if arguments.ip_range is None:
        parser.error("[-] Please specify range (-r) argument")
    return arguments.ip_range


def print_devices(data):
    print("IP\t\t\t| MAC Address")
    print("-------------------------------------------")
    for s in data:
        print(s["ip"] + "\t\t| " + s["mac"])


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return [{"ip": s[1].psrc, "mac": s[1].hwsrc} for s in answered]


ip_range = parse_arguments()
data = scan(ip_range)
print_devices(data)
