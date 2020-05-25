# -*- coding: utf-8 -*-

import time
from datetime import datetime
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import Config, IPS, IPort, LivingIP, Admin

from utils import tools

# 创建连接相关
# 初始化数据库链接
# 和 sqlapi 交互，执行转换后的 sql 语句，用于创建基类
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(bind=engine)
session = Session()
session2 = Session()




def finger_scan(model):
    '''
    指纹扫描；使用nmap的两种扫描方式探测指纹信息。1.重量级扫描，慢数据准确。2.无ping扫描速度快
    :param model: nmap\version-all
    :return:
    '''
    print('[+] 开始探测端口指纹信息，模式{}'.format(model))
    from scan_tools.script.nmap_top import NmapScan
    ip_list = session.query(LivingIP).filter(LivingIP.flag == '1').all()
    for i in ip_list:
        ip =i.ip
        ports =','.join( port.port for port in i.living_port)
        '''
        找到一个存活ip下所有的端口。将数据交给namp扫描
        '''
        if ports:
            ns =NmapScan(model=model)
            finger_info = ns.run(ip=ip,port=ports)
            if not finger_info:return False
            for port in list(finger_info.keys()):

                port_finger =finger_info.get(port)
                print(port_finger)
                port_finger_db =session.query(IPort).filter_by(ip=i.id,port=str(port)).first()
                port_finger_db.finger_name=port_finger.get('name')
                port_finger_db.finger_state=port_finger.get('state')
                port_finger_db.finger_product=port_finger.get('product')
                port_finger_db.finger_version=port_finger.get('version')
                port_finger_db.finger_extrainfo=port_finger.get('extrainfo')
                port_finger_db.finger_cpe=port_finger.get('cpe')
                port_finger_db.status=port_finger.get('state')
                port_finger_db.flag='1'
                port_finger_db.scan_time=datetime.now()
                session.commit()

    return True


def port_scan(model):
    '''
    端口探测：模式socket模式与masscan模式，（分别为全端口与敏感端口探测）
    默认是socket敏感端口探测
    :param model: socket_all、socket_vul、masscan_all、masscan_vul
    :return:
    '''
    print('[+] 开始探测port存活，模式{}'.format(model))
    from scan_tools.script import socket_all, socket_vul, msscan_all, msscan_vul
    ip_list = session.query(LivingIP).filter(LivingIP.flag == '1').all()
    '''
    获取到数据库中所有存活的ip，
    '''
    conf = session.query(Config).first()
    if not ip_list: return False
    for ip_obj in ip_list:
        living_port = []
        '''
        选择不同的模式
        '''
        if model == 'socket-all':
            sa = socket_all.SocketAll()
            try:
                living_port = sa.run(ip=ip_obj.ip,thread=conf.thread)
            except:
                living_port = []
        elif model == 'socket-vul':
            sv = socket_vul.SocketVul(ports=conf.vul_port)
            living_port = sv.run(ip=ip_obj.ip)
        elif model == 'masscan-all':
            ma = msscan_all.MasscanAll()
            try:
                living_port = ma.run(ip=ip_obj.ip, thread=conf.thread)
            except:
                living_port = []
        elif model == 'masscan-vul':
            mv = msscan_vul.MasscanVul(ports=conf.vul_port)
            living_port = mv.run(ip=ip_obj.ip, thread=conf.thread)

        else:
            port_scan(model='socket-vul')
        print(ip_obj.ip, living_port)
        '''
        遍历所有存活的端口
        '''
        for port in living_port:
            if not session.query(IPort).filter(IPort.ip == ip_obj.id, IPort.ips == ip_obj.ips,
                                               IPort.port == port).first():
                iprot = IPort(ip=ip_obj.id, ips=ip_obj.ips, port=port, status='1')
                session.add(iprot)
                session.commit()
    return True


def living_scan(model):
    '''
    探测存活的模式：ping模式与icmp模式
    :param model: ping icmp
    :return:
    '''
    print('[+] 开始探测ip存活，模式{}'.format(model))
    from scan_tools.lib import icmp, alive,arp_scan
    '''
    获取到数据库所有的ip列表
    '''
    ip_list = session.query(LivingIP).all()
    if not ip_list: return False

    if model == 'ping':
        for ip in ip_list:
            '''
            传入每一个进行ip ping访问。如果ping同返回True，同时更新扫描时间 否则返回false         '''
            if alive.winping(ip.ip):
                ip.flag = '1'  # flag=1 代表存活
            else:
                ip.flag = '0'
            ip.scan_time = datetime.now()
            session.commit()
    elif model == 'icmp':
        ipPool = []
        for ip in ip_list:
            ipPool.append(ip.ip)
        '''
        icmp的检测方式更快，我们传入的是一个ip列表池，所以将ip加入列表中
        '''
        s = icmp.Nscan()
        living_ip_dict = s.mPing(ipPool)
        if living_ip_dict:
            for i in ip_list:
                '''
                查询ip库中的ip=ip
                '''
                living_ip = session.query(LivingIP).filter(LivingIP.ip == i.ip).first()
                living_ip.scan_time = datetime.now()
                if i.ip in living_ip_dict:
                    living_ip.flag = '1' # 存活的ip标志为1
                else:
                    living_ip.flag = '0'
            session.commit()
    elif model=='arp':
        ipPool = []
        for ip in ip_list:
            ipPool.append(ip.ip)
        _as =arp_scan.ArpScan()
        living_ip_dict =_as.run(ipPool)
        if living_ip_dict:
            for i in ip_list:
                '''
                查询ip库中的ip=ip
                '''
                living_ip = session.query(LivingIP).filter(LivingIP.ip == i.ip).first()
                living_ip.scan_time = datetime.now()
                if i.ip in living_ip_dict:
                    living_ip.flag = '1'  # 存活的ip标志为1
                else:
                    living_ip.flag = '0'
            session.commit()
    else:
        # 如果模式不对，默认选择ping方式
        model = 'ping'
        living_scan(model=model)
    return True


def ip_to_list():
    '''
    将ip、段、子网转化成单独的ip
    :return:
    '''
    ips = session.query(IPS).filter_by(status='1').all()
    from scan_tools.lib.iplist import IPinfo
    if not ips:
        return False
    '''
    将ip、段、子网转换成单独的ip的列表
    '''
    for ip in ips: # 数据库中的带扫描的网段
        for i in IPinfo(ip.ips):
            '''
            如果数据库没有这个ip地址，第一次添加的，那么加入到数据库中
            '''
            if not (session.query(LivingIP).filter(LivingIP.ip == i).first()):
                living_ip = LivingIP(ips=ip.id, ip=i)
                session.add(living_ip)

            else:
                '''
                '''
                ip.scan_time=datetime.now()
        ip.flag = '1'
    session.commit()

    return True


def check_config():
    '''
    第一次初始化的时候，为配置添加一个初始变量
    :return:
    '''
    conf = session.query(Config).first()
    now_time = int(time.time())
    spider_time = int(time.mktime(
        time.strptime(time.strftime("%Y-%m-%d", time.localtime(now_time)), "%Y-%m-%d"))+eval(config.LOOP_TIME))

    if not conf:

        conf = Config(create_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(spider_time)),
                      )
        session.add(conf)
        session.commit()
        return False
    else:
        spider_time = int(time.mktime(
            time.strptime(time.strftime("%Y-%m-%d", time.localtime(now_time)), "%Y-%m-%d")) + eval(conf.loop_time))

        conf.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(spider_time))
        session.commit()
        return True


def run():
    # 先判断是否有config数据
    check_config()
    monitor()
    print('[+] 监控资产……')
    time.sleep(3)
    while True:

        # 判断是否到达采集的时间。
        conf = session.query(Config).first()
        now_time = int(time.time())
        is_add_ip =session.query(IPS).filter(IPS.flag==None,IPS.status=='1').first()
        if now_time > (conf.create_time.timestamp()) or is_add_ip:
            print('[+] 开始探测资产')
            # check_defense()
            # 0. 整理输入ip资产
            ip_to_list()
            # 1.首先探测存活
            living_scan(model=conf.living_model)
            # 2.探测端口开放情况
            port_scan(model=conf.port_model)
            # 3.探测端口指纹信息
            finger_scan(model=conf.finger_model)
            # check_dodcio()
            # 周期内采集结束，时间更新为最近时间
            conf = session.query(Config).first()
            conf.create_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(conf.create_time.timestamp() + eval(conf.cycle_time)))
            session.commit()
            print('[+] 下次扫描时间',
                  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(conf.create_time.timestamp())))
        time.sleep(eval(conf.sleep_time))  # 扫描周期

    # 回调page+1
import threading

def engine_living():
    while 1:
        # print('引擎活着')
        conf = session2.query(Config).first()
        conf.engine = datetime.now()
        session2.commit()
        # time.sleep(eval(conf.sleep_time))
        time.sleep(5)

def monitor():
    '''
    监控 扫描引擎是否运行
    :return:
    '''
    threads=[]
    for i in range(1):
        t = threading.Thread(target=engine_living, )
        threads.append(t)
        t.start()
    #
    # for t in threads:
    #     t.join()
    #


if __name__ == '__main__':
    print('[+] 开启资产监控扫描')
    run()

    # ip_to_list()
    # living_scan('icmp')
    # port_scan(model='socket_vul')
    # finger_scan('nmap')
