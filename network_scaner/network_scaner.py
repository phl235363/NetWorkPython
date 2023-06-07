#!/usr/bin/env python
import scapy.all as scapy
import argparse

def scan(ip):
    #tao goi arp va ethernet
    arp_request = scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #ket hop 2 goi tin de gui cho toan mang 
    arp_request_broascast=broadcast/arp_request
    #gui goi tin va nhan ve phan hoi 
    answered_list=scapy.srp(arp_request_broascast,timeout= 1)[0]
    scapy.sr1(time=20)

    #format lai thong tin
    client_list=[]
    for element in answered_list:
        client_dics={"ip": element[1].psrc,"mac": element[1].hwsrc }
        client_list.append(client_dics)
    return client_list
    
def print_result(result_list):
    print ("IP\t\t\tMAC Address")
    for client in result_list:
        print (client["ip"]+"\t\t"+client["mac"])
        print("---------------------------------------")

def get_argument():
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target", help="Your target IP / Range")
    options= parser.parse_args()
    if not options.target:
        parser.error("[-] Please specific target , use --help to more info ")
    return options
options=get_argument()
result=scan (options.target)
print_result(result)
