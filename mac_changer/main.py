#!/usr/bin/env python3

import subprocess
import optparse
import re


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address for")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address to be set")
    options = parser.parse_args()[0]
    if options.interface is None:
        parser.error("[-] Please specify interface (-i option)")
    if options.new_mac is None:
        parser.error("[-] Please specify mac (-m option)")
    return options


def validate_result(interface, mac):
    output = str(subprocess.check_output(["ifconfig", interface]))
    current_mac = re.search(r"ether ([0-9a-f]{2}:){5}[0-9a-f]{2}", output).group(0)[6:]

    if mac != current_mac:
        print("[-] Something went wrong. MAC wasn't changed!")
    else:
        print("[+] MAC successfully changed to " + str(current_mac))


arguments = get_arguments()
change_mac(arguments.interface, arguments.new_mac)
validate_result(arguments.interface, arguments.new_mac)