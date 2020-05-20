# -*- coding: UTF-8 -*-
__author__ = 'Joynice'

from wtforms import (
    Form,
    StringField,
    IntegerField
)
from wtforms.validators import (
    InputRequired,
    Length, Regexp,
    ValidationError
)


class BaseForm(Form):
    def get_error(self):
        message = None
        print(self.errors)
        if self.errors == {}:
            pass
        else:
            message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super(BaseForm, self).validate()

#登录验证
class LoginForm(BaseForm):
    email = StringField(validators=[InputRequired('请输入邮箱或者用户名')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码'), InputRequired(message='请输入密码')])
    remember = IntegerField()



class AnnouncementForm(BaseForm):
    title = StringField(validators=[Regexp(r'^[\S]{1,20}', message='请输入正确格式的标题'), InputRequired(message='请输入标题！')])
    content = StringField(validators=[Regexp(r'^[\S]{1,300}', message='请输入正确格式的内容'), InputRequired(message='请输入内容！')])

class MsgBoardForm(BaseForm):
    content = StringField(validators=[Regexp(r'^[\S]{1,200}', message='请输入正确格式的内容'), InputRequired(message='请输入内容！')])
    graph_captcha = StringField(
        validators=[Regexp(r'\w{4}', message='请输入正确格式的图形验证码！'), InputRequired(message='请输入验证码')])

    def validate_graph_captcha(self, field):
        from utils import zlcache
        graph_captcha = field.data
        graph_captcha_mem = zlcache.get(graph_captcha.lower())
        if not graph_captcha_mem:
            raise ValidationError(message='图形验证码错误！')
        else:
            zlcache.delete(graph_captcha.lower())
