from flask import render_template, request, session, redirect, url_for
from datetime import timedelta
from DialectsProtecting import app, database, currentUsername, currentPassword

import os

#session有效期为1天
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
#设置秘钥为随机24字节的数
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
@app.route('/home')
def home():

    return render_template(
        'user.html',
    )

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
            return render_template('/login.html', errorStatus = 1)
        elif status == 0:
            return render_template('/login.html', errorStatus = 0)

    elif request.method == 'GET':
        #访问登录页面
        return render_template('/login.html', errorStatus = 2)


#检验用户名有效性
def checkUsernameValidity(username):
    #用户名长度不得小于4
    if len(username) < 4:
        return False
    else:
        return True

#检验密码有效性
def checkPasswordValidity(password):
    #密码长度不得小于6
    if len(password) < 6:
        return False
    else:
        return True

#注册界面
@app.route('/register', methods=['GET', 'POST'])
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

        status = database.register(username, password)
        if (status == 0):
            #用户名已经存在
            return render_template('/register.html', errorStatus = 0)
        elif (status == 1):
            #注册后自动登录成功，保存session
            session['username'] = username
            session['password'] = password
            #返回主页
            return redirect(url_for('home'))

    elif request.method == 'GET':
        #访问注册页面
        return render_template('/register.html', errorUsername = False)

@app.route('/user')
def user():
    return render_template(
        'user.html',
    )

