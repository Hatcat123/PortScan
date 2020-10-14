#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'AJay'
__mtime__ = '2020/5/25 0025'

"""
#局域网主机扫描器 使用ARP扫描
#主机扫描

#encoding=utf-8
from scapy.all import *
import threading



class ArpScan():
    def __init__(self):
        self.portdict = []
        self.threads = []
    def run(self,ip):
        self.arp_scan(ip)
        return self.portdict

    def arp_scan(self,ip):
        for i in ip:
            t = threading.Thread(target=self.scan, args=((i,)))
            self.threads.append(t)
            t.start()
        for t in self.threads:
            t.join()

    def scan(self,target_ip):
        '''
        通过scapy的sr1函数进行ARP扫描
        '''
        try:
        # if 1==1:
            ans = sr1(ARP(pdst=target_ip), timeout=1, verbose=False)
            if ans:
                self.portdict.append(target_ip)
                return True
        except Exception:
            print('[-]发包错误')

if __name__ == '__main__':
    ip = ['192.168.199.102','192.168.199.1','192.168.199.162','10.63.2.126']

    _as =ArpScan()
    print('存活ip',_as.run(ip))