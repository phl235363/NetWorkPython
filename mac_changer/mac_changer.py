#!/usr/bin/env python3

import subprocess
import optparse
import re


def change_mac(interface,new_mac):
    print("[+] changing MAC address for "+ interface+ " to " + new_mac)
    subprocess.call(["sudo","ifconfig",interface,"down"])
    subprocess.call(["sudo","ifconfig", interface,"hw","ether",new_mac])
    subprocess.call(["sudo","ifconfig",interface,"up"])
 
    print("done") 
def get_arguments ():
    parse = optparse.OptionParser()
    parse.add_option("-i","--interface",dest="interface",help ="Interface to change MAC")
    parse.add_option("-m","--mac",dest="new_mac",help= "MAC want to chagne " ) 
    (options,arguments )=parse.parse_args()
    if not options.interface:
        parse.error("[-] Please specific interface , use --help to more info ")
    if not options.new_mac :
        parse.error("[-] Please specific new_mac , use --help to more info ")
    return  options
def get_current_mac(interface):
    ifconfig_result =subprocess.check_output(["ifconfig",options.interface])
    mac_address_search_result=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print ("Can't read MAC address")
# #get option 
options=get_arguments()
#get current mac
current_mac= get_current_mac(options.interface)
print ("current mac: " + str(current_mac))

# #change mac 
change_mac(options.interface, options.new_mac)
current_mac=get_current_mac(options.interface)

if current_mac == str(options.new_mac):
    print("[+] Change MAC sucessful !")
else:
    print(options.new_mac)
    print("[-] Can not change mac")

