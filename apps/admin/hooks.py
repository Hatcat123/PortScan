# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

# 钩子函数
from .views import bp
from flask import session, g, render_template
from models import Admin
# from config import config
from flask import current_app


@bp.before_request
def before_request():
    if current_app.config['CMS_USER_ID'] in session:
        user_id = session.get(current_app.config['CMS_USER_ID'])
        user = Admin.query.get(user_id)

        if user:
            g.user = user

    else:
        g.user = {"username": '旅行者'}


@bp.errorhandler(404)
def page_not_found(error):
    if current_app.config['CMS_USER_ID'] in session:
        user_id = session.get(current_app.config['CMS_USER_ID'])
        user = Admin.query.get(user_id)
        if user:
            g.user = user
    return render_template('admin/admin_404.html'), 404
