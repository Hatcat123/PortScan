import datetime

from flask import (
    Blueprint,
    views,
    render_template,
    session,
    request,
    redirect,
    url_for,
    current_app
)
from sqlalchemy import and_

from exts import db
from models import Admin, Config, IPort, IPS, LivingIP
from utils import field
from .decorators import login_required
from .forms import LoginForm
from utils import tools
bp = Blueprint('admin', __name__, url_prefix='/admin')


# 登录页面
class LoginView(views.MethodView):

    def get(self):
        message = request.args.get('message')
        return render_template('admin/login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data  # 邮箱或者用户名
            password = form.password.data
            remember = form.remember.data
            user = Admin.query.filter_by(email=email).first() or Admin.query.filter_by(username=email).first()
            if user and user.check_password(password):
                session[current_app.config['CMS_USER_ID']] = user.id  # 保存用户登录信息
                if remember:
                    # 如果设置session.permanent = True，那么过期时间为31天
                    session.permanent = True
                user.last_login_time = datetime.datetime.now()
                db.session.add(user)
                db.session.commit()
                return field.success(message='登陆成功！')
            else:
                return field.params_error(message='邮箱或者密码错误')

        else:
            message = form.get_error()
            return field.params_error(message=message)


# 注销
class LogoutView(views.MethodView):
    decorators = [login_required]

    def get(self):
        del session[current_app.config['CMS_USER_ID']]
        return redirect(url_for('admin.login'))

    def post(self):
        pass


# 后台首页
class IndexView(views.MethodView):
    decorators = [login_required]

    def get(self):
        ips_num = IPS.query.count()  # 资产数量
        monitor_ips_num = IPS.query.filter_by(status='1').count()  # 监控资产数量
        ip_num = LivingIP.query.filter_by(flag='1').count()  # ip资产数量
        port_num = IPort.query.filter_by(flag='1').count()  # 端口数量
        context = {
            'ips_num': ips_num,  # 资产数量
            'monitor_ips_num': monitor_ips_num,  # 监控资产数量
            'ip_num': ip_num,  # ip资产数量
            'port_num': port_num,  # 端口数量
        }
        return render_template('admin/admin_index.html', **context)

    def post(self):
        pass


# IPS展示
class IPSView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('admin/ips.html')

    def post(self):
        page = int(request.form.get('page'))
        limit = int(request.form.get('limit'))
        start = (page - 1) * limit
        end = start + limit

        ips_obj = IPS.query.order_by(IPS.create_time.asc())
        ips = ips_obj.slice(start, end)
        count = ips_obj.count()
        ips_list = []
        for ips in ips:
            ip_dict = {}
            ip_dict['id'] = ips.id
            ip_dict['ips'] = ips.ips
            ip_dict['status'] = ips.status
            ip_dict['scan_time'] = str(ips.scan_time)
            ip_dict['create_time'] = str(ips.create_time)
            ips_list.append(ip_dict)
        return field.layui_success(data=ips_list, count=count)


# IPS添加
class AddIPSView(views.MethodView):
    decorators = [login_required]

    def post(self):
        ips = request.form.get('ips')

        if ips:
            is_exc = IPS.query.filter(IPS.ips == ips).first()
            if not is_exc:
                new_ips = IPS(ips=ips)
                db.session.add(new_ips)
                db.session.commit()
                return field.success(message='{}添加成功！'.format(ips))
            return field.params_error(message='添加失败！')
        return field.params_error(message='添加失败！')


# IPS删除
class DelIPSView(views.MethodView):
    decorators = [login_required]

    def post(self):
        data = request.values
        id = data.get('id')
        del_ips = IPS.query.filter(IPS.id == id).first()
        if del_ips:
            db.session.delete(del_ips)
            db.session.commit()
            return field.success(message='删除成功！')
        return field.params_error(message='删除失败！')


# 改变IPS资产状态
class ChangeIPSView(views.MethodView):
    decorators = [login_required]

    def post(self):
        data = request.values
        print(data)
        get_id = data.get('id')
        status = data.get('status')
        ips = IPS.query.filter(IPS.id == get_id).first()
        if ips:
            if status:
                if ips.status != status:
                    ips.status = status

                db.session.commit()
                return field.success(message='修改成功！')
            return field.params_error(message='修改失败！')
        return field.params_error(message='修改失败！')


# 存活IP展示
class LivingIPView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('admin/livingip.html')

    def post(self):
        data = request.values
        keys = list(data.keys())
        keys.remove('page')
        keys.remove('limit')

        page = int(request.form.get('page'))
        limit = int(request.form.get('limit'))
        start = (page - 1) * limit
        end = start + limit

        livingip_obj = LivingIP.query.order_by(LivingIP.create_time.asc())
        print(keys)
        if keys:

            if data.get('all') == '1':
                livingip_search = livingip_obj.filter(
                    and_(LivingIP.ip.like("%" + data.get('ip', '') + "%"),
                         ))
            else:
                livingip_search = livingip_obj.filter(
                    and_(LivingIP.ip.like("%" + data.get('ip', '') + "%"),

                         )).filter(LivingIP.flag == '1')
        else:
            livingip_search = livingip_obj.filter(LivingIP.flag == '1')

        ips = livingip_search.slice(start, end)
        count = livingip_search.count()
        ips_list = []
        for ips in ips:
            ip_dict = {}
            ip_dict['id'] = ips.id
            ip_dict['ips'] = ips.IPS.ips
            ip_dict['ip'] = ips.ip
            ip_dict['status'] = ips.flag
            ip_dict['scan_time'] = str(ips.scan_time)
            ip_dict['create_time'] = str(ips.create_time)
            ips_list.append(ip_dict)
        return field.layui_success(data=ips_list, count=count, message='查询成功')


# 开放端口展示
class IPortView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('admin/iport.html')

    def post(self):

        data = request.values
        keys = list(data.keys())
        keys.remove('page')
        keys.remove('limit')

        page = int(request.form.get('page'))
        limit = int(request.form.get('limit'))
        start = (page - 1) * limit
        end = start + limit

        iport_obj = IPort.query.order_by(IPort.create_time.asc())

        if keys:
            print(data.get('name'))
            iport_search = iport_obj.filter(
                and_(
                    IPort.port.like("%" + data.get('port', '') + "%"),
                    IPort.finger_name.like("%" + data.get('name', '') + "%"),
                )).filter(IPort.flag == '1')

        else:

            iport_search = iport_obj.filter(IPort.flag == '1')

        ips = iport_search.slice(start, end)
        count = iport_search.count()
        ips_list = []
        for ips in ips:
            ip_dict = {}
            ip_dict['id'] = ips.id
            ip_dict['ips'] = ips.SIPS.ips
            ip_dict['ip'] = ips.living_port.ip
            ip_dict['port'] = ips.port
            ip_dict['finger'] = ips.finger
            ip_dict['finger_name'] = ips.finger_name
            ip_dict['finger_state'] = ips.finger_state
            ip_dict['finger_product'] = ips.finger_product
            ip_dict['finger_version'] = ips.finger_version
            ip_dict['finger_extrainfo'] = ips.finger_extrainfo
            ip_dict['finger_cpe'] = ips.finger_cpe

            ip_dict['status'] = ips.status
            ip_dict['scan_time'] = str(ips.scan_time)
            ip_dict['create_time'] = str(ips.create_time)
            ips_list.append(ip_dict)
        return field.layui_success(data=ips_list, count=count, message='查询成功')


# 系统设置
class SystemView(views.MethodView):
    decorators = [login_required]

    def get(self):
        config = Config.query.first()

        if (datetime.datetime.now() - config.engine).seconds <= 5:
            engine = True
        else:
            engine = False
        system = {
            "create_time": config.create_time,
            "loop_time": config.loop_time,
            "cycle_time": config.cycle_time,
            "sleep_time": config.sleep_time,
            "living_model": config.living_model,
            "port_model": config.port_model,
            "finger_model": config.finger_model,
            "vul_port": config.vul_port,
            "thread": config.thread,
            "engine": engine,
        }
        return render_template('admin/admin_system.html', system=system)

    def post(self):
        data = request.values
        config = Config.query.first()
        print(data.get('loop_time'))
        config.loop_time = data.get('loop_time')
        config.cycle_time = data.get('cycle_time')
        config.sleep_time = data.get('sleep_time')
        config.living_model = data.get('living_model')
        config.port_model = data.get('port_model')
        config.finger_model = data.get('finger_model')
        config.vul_port = data.get('vul_port')
        config.thread = data.get('thread')

        db.session.commit()
        return redirect(url_for('admin.system'))

class BarChart1View(views.MethodView):
    decorators = [login_required]

    def get(self):
        c = tools.server_pie()
        return c.dump_options()

    def post(self):
        pass

class BarChart2View(views.MethodView):
    decorators = [login_required]

    def get(self):
        c = tools.port_pie()
        return c.dump_options()

    def post(self):
        pass

# 登录、登出、首页
bp.add_url_rule('login/', view_func=LoginView.as_view('login'))  # 后台登录页面
bp.add_url_rule('logout/', view_func=LogoutView.as_view('logout'))  # 后台登录页面
bp.add_url_rule('/', view_func=IndexView.as_view('index'))  # 后台登录页面

# 资产管理
bp.add_url_rule('ips/', view_func=IPSView.as_view('ips'))  # 展示资产
bp.add_url_rule('add_ips/', view_func=AddIPSView.as_view('add_ips'))  # 添加资产
bp.add_url_rule('del_ips/', view_func=DelIPSView.as_view('del_ips'))  # 删除资产
bp.add_url_rule('change_ips/', view_func=ChangeIPSView.as_view('change_ips'))  # 改变资产状态

# ip展示

bp.add_url_rule('livingip/', view_func=LivingIPView.as_view('livingip'))  # 展示资产

# 端口与指纹展示
bp.add_url_rule('iport/', view_func=IPortView.as_view('iport'))  # 展示端口/指纹


# 系统模块
bp.add_url_rule('system/', view_func=SystemView.as_view('system'))  # 系统配置

# 统计图
bp.add_url_rule('barChart1/', view_func=BarChart1View.as_view('barChart1'))  # 服务统计图
bp.add_url_rule('barChart2/', view_func=BarChart2View.as_view('barChart2'))  # 端口统计图

