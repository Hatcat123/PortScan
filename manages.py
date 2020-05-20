
# -*- coding: utf-8 -*-


from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from app import app  # 进行部分数据库初始化

from exts import db
from models import Admin


manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 创建后台管理员用户
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_admin(username, password, email):
    # avatar = GithubAvatarGenerator()
    # path = '..' + sep +'static'+ sep+ 'admin'+sep +'image'+ sep + email +'.png'
    # avatar.save_avatar(filepath='.' + sep +'static'+ sep+ 'admin'+sep +'image'+ sep + email +'.png')
    user = Admin(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('Admin添加成功！！！')



if __name__ == '__main__':
    manager.run()
