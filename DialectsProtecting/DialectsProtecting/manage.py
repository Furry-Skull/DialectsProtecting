# encoding: utf-8

from flask import render_template, session

from DialectsProtecting import app
from DialectsProtecting.user import user
from DialectsProtecting.my import my
from DialectsProtecting.search import search
from DialectsProtecting.detail import detail
from DialectsProtecting.database import db


#注册蓝图，新增模块在这里注册
app.register_blueprint(user, url_prefix = '/user')
app.register_blueprint(my, url_prefix = '/my')
app.register_blueprint(search, url_prefix = '/search')
app.register_blueprint(detail, url_prefix = '/detail')

#主页
@app.route('/')
@app.route('/home')
def home():
    #方言语系的对应关系请在这里添加
    db.insertLanguage('吴语','杭州话')
    db.userLike(1,1)
    db.userDislike(1,1)
    #获取用户状态，显示页面
    return render_template('home.html')

#404页面
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('page404.html'), 404