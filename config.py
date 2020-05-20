# -*- coding: utf-8 -*-

import os
import random
base_path =os.path.dirname(os.path.abspath(__file__))

nmap_path =os.path.join(base_path,'port_scan','bin','nmap.exe')
masscan_path =os.path.join(base_path,'port_scan','bin','masscan.exe')
SECRET_KEY = 'DROPS'
CMS_USER_ID = 'DSADSA6jvxE2MeiZ5NnvJorNbN3XD1551512'

# mysql设置
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'port_scan'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(MYSQL_USERNAME, MYSQL_PASSWORD,
                                                                               MYSQL_HOST, MYSQL_PORT,
                                                                               MYSQL_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = False
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE = 90

# 系统配置

LOOP_TIME = '3 * 60 * 60'  # 采集周期为每天几点采集。24小时制。如`18 * 60 * 60`每天18:00开始采集

CYCLE_TIME = '6*60 * 60'  # 循环周期。每12个小时采集一次

SLEEP_TIME = '1 * 60 ' # 监测周期

# 危险脆弱端口
VUL_PORTS = "21,22,23,25,80,161,389,443,445,512,513,514,873,1025,111,1433,1521,5560,7778,2601,2604,3128,3306,3312,3311,3389,4440,5432,5900,5984,6082,6379,7001,7002,7778,8000,8001,8080,8089,8090,9090,8083,8649,8888,9200,9300,10000,11211,27017,27018,28017,50000,50070,50030"

living_model=random.choice(['icmp','ping'])
port_model=random.choice(['socket_all','socket_vul','masscan_all','masscan_vul'])
finger_model=random.choice(['namp','version-all'])