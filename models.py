# -*- coding: utf-8 -*-
from exts import db
import datetime
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash

import config
from exts import db
import datetime

class Admin(db.Model):
    '''
    管理员类
    '''
    __tablename__ = 't_admin'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(20))
    join_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_login_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(Admin, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)




class Config(db.Model):
    '''
    配置信息：最近采集时间、采集模式
    '''
    __tablename__ = 't_config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loop_time = db.Column(db.String(255), default=config.LOOP_TIME,comment='采集周期为每天几点采集')
    cycle_time = db.Column(db.String(255), default=config.CYCLE_TIME,comment='循环周期。每12个小时采集一次')
    sleep_time = db.Column(db.String(255), default=config.SLEEP_TIME,comment='监测周期')
    living_model = db.Column(db.String(255), default=config.living_model,comment='选择ip存活模块检测模块')
    port_model = db.Column(db.String(255), default=config.port_model,comment='选择端口检测模块')
    finger_model = db.Column(db.String(255), default=config.finger_model,comment='选择指纹检测模块')
    vul_port = db.Column(db.String(1000), default=config.VUL_PORTS, comment='敏感端口')
    thread = db.Column(db.Integer, default=1000, comment='扫描线程')
    engine = db.Column(db.DateTime, default=datetime.datetime.now,  comment='扫描引擎下次巡检时间')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='采集时间')



class IPS(db.Model):
    '''
    添加的资产信息
    '''
    __tablename__ = 't_ips'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ips = db.Column(db.String(255), comment='ip地址或者网段')
    flag = db.Column(db.String(255), comment='采集成功标志，0or1')
    status = db.Column(db.String(255), default='0', comment='状态是否采集，默认为0 ，0or1')
    scan_time = db.Column(db.DateTime,  comment='最近扫描时间')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')

    living_ip = db.relationship('LivingIP', backref='IPS', lazy=True)
    iport = db.relationship('IPort', backref='SIPS', lazy=True)


class LivingIP(db.Model):
    '''
    存活的ip信息
    '''
    __tablename__ = 't_living_ip'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ips = db.Column(db.Integer, db.ForeignKey('t_ips.id'))
    ip = db.Column(db.String(255), comment='具体ip地址')
    flag = db.Column(db.String(255), comment='采集成功标志，0or1')
    status = db.Column(db.String(255), default='0', comment='状态是否采集，默认为0 ，0or1')
    scan_time = db.Column(db.DateTime, comment='最近扫描时间')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')

    living_port = db.relationship('IPort', backref='living_port', lazy=True)

class IPort(db.Model):
    '''
    存活的ip信息端口存活状态
    '''
    __tablename__ = 't_iport'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ips = db.Column(db.Integer, db.ForeignKey('t_ips.id'))
    ip = db.Column(db.Integer, db.ForeignKey('t_living_ip.id'))
    # ip = db.Column(db.String(255), comment='具体ip地址')
    port = db.Column(db.String(255), comment='具体ip地址')
    finger= db.Column(db.String(255), comment='指纹')
    finger_name= db.Column(db.String(255), comment='指纹端口名称')
    finger_state= db.Column(db.String(255), comment='指纹端口状态')
    finger_product= db.Column(db.String(255), comment='指纹端口设备')
    finger_version= db.Column(db.String(255), comment='指纹端口版本')
    finger_extrainfo= db.Column(db.String(255), comment='指纹端口额外信息')
    finger_cpe= db.Column(db.String(255), comment='指纹端口cpe')

    flag = db.Column(db.String(255), comment='采集成功标志，0or1')
    status = db.Column(db.String(255), default='0', comment='状态是否采集，默认为0 ，0or1')
    scan_time = db.Column(db.DateTime, comment='最近扫描时间')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')


