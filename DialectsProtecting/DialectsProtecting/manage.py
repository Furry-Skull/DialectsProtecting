from flask import render_template, session
from datetime import timedelta
from os import urandom

from DialectsProtecting import app
from DialectsProtecting.user import user
from DialectsProtecting.my import my

from DialectsProtecting.user.userUtils import getUser

#服务器设置
#session有效期为1天
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
#设置秘钥为随机24字节的数
app.config['SECRET_KEY'] = urandom(24)

#注册蓝图，新增模块在这里注册
app.register_blueprint(user, url_prefix = '/user')
app.register_blueprint(my, url_prefix = '/my')

#主页
@app.route('/')
@app.route('/home')
def home():
    #测试页面
    return render_template(
        'audioDetail.html',
        audioName = None,

    )
    #获取用户状态，显示页面
    return render_template(
        'home.html',
        userName = getUser()
    )

#404页面
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('page404.html'), 404
