# -*- encoding: utf-8 -*-
'''
@File : iplist.py
@Time : 2019/08/27 22:03:33
@Author : JE2Se 
@Version : 1.0
@Contact : admin@je2se.com
@WebSite : https://www.je2se.com
'''
from IPy import IP
from ipaddr import IPAddress as ip_address

import os

ipList = []
def IPauto(ipl):
    ipr = IP(ipl) 
    for ip in ipr:
        ipList.append(str(ip))

def IPduan(ipl):
    sides = ipl.split('-')
    startip = sides[0]
    endip = sides[1]
    startip  = ip_address(startip)
    endip = ip_address(endip)
    while startip <= endip:
        ipList.append(str(startip))
        startip += 1

def IPyu(ipl):
    sides = ipl.split('-')
    startip = sides[0]
    endip = sides[1]
    ipf = IP(startip)
    ipe = IP(endip)
    startip  = ip_address(ipf[0])
    endip = ip_address(ipe[-1])
    while startip <= endip:
        ipList.append(str(startip))
        startip += 1

def IPdou(ipl):
    sides = ipl.split(',')
    for ip in sides:
        ipList.append(ip)

def IPge(ipl):
    sides = ipl.split(',')
    for ip in sides:
        if "-" in ip:
            IPyu(ip)
        else:
            ipList.append(ip)

def IPne(ipl):
    sides = ipl.split(',')
    for ip in sides:
        if "/" in ip:
            IPauto(ip)
        else:
            ipList.append(ip)

def IPal(ipl):
    sides = ipl.split(',')
    for ip in sides:
        if "/" in ip and "-" not in ip:
            IPauto(ip)
        elif "-" and "/" in ip:
            IPyu(ip)
        elif "-" in ip and "/" not in ip:
            IPduan(ip)
        else:
            ipList.append(ip)
           


def IPinfo(info):
    '''
    ip格式转化 输入ip地址转化成ip列表
    :param info:
    :return:
    '''
    if "1/24" in info:
        info = info.replace("1/24","0/24")
        try:
            if "/" in info and "-" not in info  and "," not in info:
                    IPauto(info)
            elif "-" in info and "/" not in info and "," not in info:
                IPduan(info)
            elif "-" and "/" in info and "," not in info:
                IPyu(info)
            elif "," and "/"  and "-" in info:
                IPal(info)
            elif "," in info and "-" not in info and "/" not in info :
                IPdou(info)
            elif "," and "-" in info and "/" not in info:
                IPge(info)
            elif "," and "/" in info and "-" not in info:
                IPne(info)
            else:
                ipList.append(info)
            return ipList
        except:

                       os._exit(0)
    else:
        try:
            if "/" in info and "-" not in info  and "," not in info:
                    IPauto(info)
            elif "-" in info and "/" not in info and "," not in info:
                IPduan(info)
            elif "-" and "/" in info and "," not in info:
                IPyu(info)
            elif "," and "/"  and "-" in info:
                IPal(info)
            elif "," in info and "-" not in info and "/" not in info :
                IPdou(info)
            elif "," and "-" in info and "/" not in info:
                IPge(info)
            elif "," and "/" in info and "-" not in info:
                IPne(info)
            else:
                ipList.append(info)
            return ipList
        except:
                      os._exit(0)
if __name__ == '__main__':
    print(IPinfo('192.168.1.'))
    print(IPinfo('192.168.1.168.1.10'))
    print(IPinfo('192.168.1.1/24'))
    print(IPinfo('192.168.1.0/24'))

