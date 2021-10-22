#!/usr/bin/env python3.8

import sys
from scapy.all import *
import argparse
import csv
import time

def arg_parser():
    parser = argparse.ArgumentParser(description='gtpu_data')
    parser.add_argument("-d", "--dst_mac", help="destination mac", default="42:01:0a:00:00:06")
    parser.add_argument("-e", "--enb_ip_addr", help="Enb addr", default="172.31.2.228")
    parser.add_argument("-a", "--sgw_ip_addr", help="agw s1u addr", default="54.151.101.161")
    parser.add_argument("-s", "--srv_ip_addr", help="Remote", default="8.8.8.8")
    parser.add_argument("-n", "--num_pkt", help="Number of packets per sec", type=int, default=1)
    parser.add_argument("-l", "--duration", help="duration sec", type=int, default=300)
    parser.add_argument("-i", "--eth", help="eth interface", default="eth0")
    #parser.add_argument("-i", "--icmp", help="send ICMP", type=bool, default=false)

    args = parser.parse_args()
    return args

args =  arg_parser()
srcMac = RandMAC()

srv_ip_addr_2="9.9.9.9"

lines = []
csv_file=open('/tmp/teid.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
line_count = 0
for data in csv_reader:
    lines.append(data)

duration = args.duration
for count in range(0, duration):
    print(f'entering loop {count}')
    line_count = 0
    for row in lines:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'TEID 0x{row[0]} IP addr {row[1]}')
            line_count += 1
            srv_ip_addr_2 = "8.8.8.8"
            inner_payload = IP(src=row[1],dst=args.srv_ip_addr)/ICMP()
            inner_payload_len = len(inner_payload)
            print("inner payload len " + str(hex(inner_payload_len))[2:])
            gtp = "30ff00"+str(hex(inner_payload_len))[2:]+row[0]
            print(gtp)
            myPayLoad = bytes.fromhex(gtp)
            #sendp(Ether()/IP(src=args.enb_ip_addr,dst=args.sgw_ip_addr)/UDP(sport=2152,dport=2152)/myPayLoad/IP(src=row[1],dst=args.srv_ip_addr)/UDP(sport=53,dport=53),iface=args.eth)
            sendp(Ether()/IP(src=args.enb_ip_addr,dst=args.sgw_ip_addr)/UDP(sport=2152,dport=2152)/myPayLoad/IP(src=row[1],dst=srv_ip_addr_2)/ICMP(),iface=args.eth)
            #sendp(IP(src=args.enb_ip_addr,dst=args.sgw_ip_addr)/UDP(sport=2152,dport=2152)/myPayLoad/IP(src=row[1],dst=args.srv_ip_addr)/ICMP(),iface=args.eth)

