#!/usr/bin/evn python3
from struct import pack
import   netfilterqueue
import scapy.all  as scapy
ack_list=[]
def process_packet(packet  ):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy[scapy.TCP].sport==80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print ("HTTP request")
                print(scapy_packet.show ())
        elif scapy_packet[scapy.TCP].dport==80:
            if scapy_packet[scapy.TCCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("HTTP Response")
                print (scapy_packet.show())
            
    packet.accept()

queue=netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()
    
