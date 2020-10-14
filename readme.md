## 端口扫描指纹管理系统
模块：

登录
用户登录


首页（资产展示数字，图表）

资产管理（添加资产列表）
 - 扫描时间，资产数量
 
       添加资产|删除资产|修改资产|资产检索

资产信息（ip、或者网段）
- 详情信息（ip下所有端口信息）
   - 端口下所有指纹信息
   
         资产检索|多个页面跳转|指纹详情页面展示

系统配置（扫描周期、扫描时间）

    扫描周期|扫描时间|扫描参数配置（自动）
    
现在做到展示ip端口开放数据。

需要做的内容：
- [x] ip存活展示页面（）
- [x] 端口存活展示页面（）
- [x] 指纹展示页面
- [x] 系统配置页面（下拉选择：指纹检测方式|端口检测方式|循环扫描配置）
- [x] 首页数据展示（最好加个图表，开放最多的端口，每日增加的资产，扫描引擎是否开启（时间间隔））
- [x] 将检测的方式按照类的形式重构
- [x] 筛选导出数据
- [ ] 数据大屏展示（提升阶段）


## 部署配置

**准备**
环境：windows7 python3.6+ nmap masscan
开发工具：pycharm
开发语言：python
数据库：mysql5.7+

**部署**
安装nmap与masscan到电脑，加入环境变量（不使用中文路径）。

配置config数据库。
创建数据库：utf-mb4-bin
```
数据库的ip、端口、密码、账户、数据库
```

安装环境包
```
pip install -r requiments.txt 
```

初始化数据库、迁移
```
python manages.py db init
python manages.py migrate
python manages.py upgrade
```

创建管理员账户
```
python manages.py create_admin -u 111111 -p 111111 -e 111111
```

运行扫描引擎
``` python
python run.py
```


运行web端
```
python app.py

 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 327-797-532
 * Running on http://127.0.0.1:9000/ (Press CTRL+C to quit)

```
访问  http://127.0.0.1:9000/ 

登录后台配置扫描环境

# [update] ignore /bin