from flask import render_template, session
from datetime import timedelta
from os import urandom

from DialectsProtecting import app
from DialectsProtecting.user import user
from DialectsProtecting.my import my
from DialectsProtecting.database import db

from os import environ

#服务器设置
#session有效期为1天
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
#设置秘钥为随机24字节的数
app.config['SECRET_KEY'] = urandom(24)


#注册蓝图，新增模块在这里注册
app.register_blueprint(user, url_prefix = '/user')
app.register_blueprint(my, url_prefix = '/my')


@app.route('/')
@app.route('/home')
def home():
    db
    db.importDialect('aa','sd','sd','sd')
    db.delectDialect('sdd')
    db.searchUserPublish('aa')
    print (db.accountExist(9))
    if 'username' in session:
        #服务器已有数据，说明已经登录
        return render_template(
            'home.html',
            isLogin = True,
            userName = session['username'],
        )
    else:
        #服务器没有数据，未登录
        return render_template(
            'home.html',
            isLogin = False,
        )

