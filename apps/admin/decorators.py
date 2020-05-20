# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

from flask import session, redirect, url_for
from functools import wraps
from flask import current_app


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_app.config['CMS_USER_ID'] in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin.login', message='请先进行登录！'))
    return inner