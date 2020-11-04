from flask import render_template, request, session, redirect, url_for
from DialectsProtecting.user import user
from DialectsProtecting.database import db

from DialectsProtecting.user.userUtils import *

#登录界面
@user.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        #提交登录表单
        form = request.form
        username = form["用户名"]
        password = form["密码"]

        status = db.login(username, password)
        if status == 2:
            #登录成功，保存session
            sessionLogin(username,password)
            #返回主页
            return redirect(url_for('home'))
        elif status == 1:
            return render_template('/login.html', errorStatus = 1)
        elif status == 0:
            return render_template('/login.html', errorStatus = 0)

    elif request.method == 'GET':
        #访问登录页面
        return render_template('/login.html', errorStatus = 2)

#注册界面
@user.route('/register', methods=['GET', 'POST'])
def registerPage():
    if request.method == 'POST':
        #提交注册表单
        form = request.form
        username = form["用户名"]
        password = form["密码"]

        if not checkUsernameValidity(username):
            return render_template('/register.html', errorStatus = 1)
        if not checkPasswordValidity(password):
            return render_template('/register.html', errorStatus = 2)

        status = db.register(username, password)
        if (status == 0):
            #用户名已经存在
            return render_template('/register.html', errorStatus = 0)
        elif (status == 1):
            #注册后自动登录成功，保存session
            sessionLogin(username,password)
            #返回主页
            return redirect(url_for('home'))

    elif request.method == 'GET':
        #访问注册页面
        return render_template('/register.html', errorUsername = False)