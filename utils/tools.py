# -*- coding: utf-8 -*-


import datetime
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from exts import db
from sqlalchemy import and_, extract, func, desc,or_
from models import IPort
test = '2020-05-06T14:45:00'


def change_time(t):
    '''
    将带有T字符串的时间改为 时间格式
    :param t:
    :return:
    '''
    update_time = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')
    return update_time

def Engchange_time(t):
    '''
    带有英文的日期转换
    :param t:
    :return:
    '''
    try:
        time_format = datetime.datetime.strptime(t, '%B  %d, %Y')
    except Exception as e:
        try:
            time_format = datetime.datetime.strptime(t, '%b  %d, %Y')
        except Exception as e:
            try:
                time_format = datetime.datetime.strptime(t, '%b. %d, %Y')
            except Exception as e:
                try:
                    time_format = datetime.datetime.strptime(t, '%B. %d, %Y')
                except:
                    time_format=datetime.datetime.now()
    return time_format

def server_pie():
    server = db.session.query(IPort.finger_name, func.count(IPort.id)).filter(IPort.finger_name!='').group_by(
        IPort.finger_name).order_by(desc(func.count(IPort.id))).all()

    c = (
        Pie()

            .add(
            series_name="服务名称",
            radius=["40%", "60%"],
            is_clockwise=False,
            data_pair=server,
            label_opts=opts.LabelOpts(
                position="outside", ))

            .set_global_opts(title_opts=opts.TitleOpts(title="服务名称分布", pos_left='center'),
                             legend_opts=opts.LegendOpts(type_='scroll', is_show=True, pos_left="5%", pos_top='5%',
                                                         orient="vertical"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")))

    return c


def port_pie():
    server = db.session.query(IPort.port, func.count(IPort.id)).filter(IPort.port != '').group_by(
        IPort.port).order_by(desc(func.count(IPort.id))).all()

    c = (
        Pie()

            .add(
            series_name="端口",
            radius=["40%", "60%"],
            is_clockwise=False,
            data_pair=server,
            label_opts=opts.LabelOpts(
                position="outside", ))

            .set_global_opts(title_opts=opts.TitleOpts(title="资产端口分布图", pos_left='center'),
                             legend_opts=opts.LegendOpts(type_='scroll', is_show=True, pos_left="5%", pos_top='5%',
                                                         orient="vertical"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")))

    return c
if __name__ == '__main__':
    change_time(test)
    Engchange_time('April 13, 2020')
