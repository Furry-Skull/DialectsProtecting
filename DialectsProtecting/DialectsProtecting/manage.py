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
    db.insertLanguage('吴语','上海话')
    db.insertLanguage('粤语','粤语')
    db.insertLanguage('闽语','闽南语')
    db.insertLanguage('湘语','湖南话')
    db.insertLanguage('平话','壮话')
    db.insertLanguage('客家话','客家话')
    db.insertLanguage('晋语','平遥话')
    db.insertLanguage('晋语','太原话')
    db.insertLanguage('赣语','南昌话')
    db.insertLanguage('赣语','宁都话')
    db.insertLanguage('赣语','金溪话')
    db.insertLanguage('徽语','池州话')
    db.insertLanguage('官话','北京话')
    db.insertLanguage('官话','重庆话')
    db.insertLanguage('官话','天津话')
    db.insertLanguage('官话','四川话')
    #获取用户状态，显示页面
    return render_template('home.html')

#404页面
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('page404.html'), 404