from flask import render_template, request, session, redirect, url_for
from datetime import timedelta
from DialectsProtecting import app, database, currentUsername, currentPassword

import os

#session有效期为1小时
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
#设置秘钥为随机24字节的数
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
@app.route('/home')
def home():
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

#登录界面
@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        #提交登录表单
        form = request.form
        username = form["用户名"]
        password = form["密码"]

        status = database.login(username, password)
        if status == 2:
            #登录成功，保存session
            session['username'] = username
            session['password'] = password
            #返回主页
            return redirect(url_for('home'))
        elif status == 1:
            return 'password wrong'
        elif status == 0:
            return 'username not exists'

    elif request.method == 'GET':
        #访问登录页面
        return render_template('/login.html')

#注册界面
@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    if request.method == 'POST':
        #提交注册表单
        form = request.form
        username = form["用户名"]
        password = form["密码"]

        status = database.register(username, password)
        if (status == 0):
            return 'register failed'
        elif (status == 1):
            #注册后自动登录成功，保存session
            session['username'] = username
            session['password'] = password
            #返回主页
            return redirect(url_for('home'))

    elif request.method == 'GET':
        #访问注册页面
        return render_template('/register.html')

#提交登录信息
@app.route('/form/login', methods=(["POST"]))
def loginForm():
    form = request.form
    username = form["用户名"]
    password = form["密码"]

    status = database.login(username, password)
    if status == 2:
        #登录成功
        session['username'] = username
        session['password'] = password
        return 'login success'
    elif status == 1:
        return 'password wrong'
    elif status == 0:
        return 'username not exists'

#提交注册信息
@app.route('/form/register', methods=(["POST"]))
def registerForm():
    form = request.form
    username = form["用户名"]
    password = form["密码"]

    status = database.register(username, password)
    if (status == 0):
        return 'register failed'
    elif (status == 1):
        return 'register successfully'