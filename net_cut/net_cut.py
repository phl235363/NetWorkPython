#!/usr/bin/evn python3


import netfilterqueue
import scapy.all as scapy 
def process_packet(packet ):
    print(packet)
    scapy_packet=scapy.IP(packet.get_payload())
    print(scapy_packet.show())
    packet.accept()
queue=netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()