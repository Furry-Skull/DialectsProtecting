from flask import render_template, request, session, redirect, url_for, abort
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
            return render_template('/login.html', userName = getUser(), errorStatus = 1)
        elif status == 0:
            return render_template('/login.html', userName = getUser(), errorStatus = 0)

    elif request.method == 'GET':
        #访问登录页面
        return render_template('/login.html', userName = getUser(), errorStatus = 2)

#注册界面
@user.route('/register', methods=['GET', 'POST'])
def registerPage():
    if request.method == 'POST':
        #提交注册表单
        form = request.form
        username = form["用户名"]
        password = form["密码"]

        if not checkUsernameValidity(username):
            return render_template('/register.html', userName = getUser())
        if not checkPasswordValidity(password):
            return render_template('/register.html', userName = getUser())

        status = db.register(username, password)
        if (status == 0):
            #用户名已经存在
            return render_template('/register.html', userName = getUser())
        elif (status == 1):
            #注册后自动登录成功，保存session
            sessionLogin(username,password)
            #返回主页
            return redirect(url_for('home'))

    elif request.method == 'GET':
        #访问注册页面
        return render_template('/register.html', userName = getUser())

#ajax请求：检测用户名是否合法
@user.route('/checkUserName', methods=['GET'])
def checkUserName():
    username = request.values.get('username')
    if username == None:
        return render_template('/page404.html')
    #检查用户名是否存在
    if not checkUsernameValidity(username):
        return '用户名至少为2位'
    if db.accountExist(username):
        return '用户名已存在'
    return '用户名合法'
