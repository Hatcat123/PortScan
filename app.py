# -*- coding: utf-8 -*-


from flask import Flask, send_from_directory, request, render_template
from sqlalchemy import and_
import datetime
import config
from exts import db
from utils import field
from sqlalchemy import extract
from apps.admin import bp as admin_bp
app = Flask(__name__)

app.config.from_object(config)  # 初始化开发环境配置1
app.register_blueprint(admin_bp)
db.init_app(app)


if __name__ == '__main__':
    app.run(port=9000, host='127.0.0.1', debug=True)
