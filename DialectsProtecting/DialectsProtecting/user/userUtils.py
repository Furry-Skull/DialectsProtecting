#用户相关操作，主要管理session

from flask import session

#登录账户，在session留下记录
def sessionLogin(username, password):
    session['username'] = username
    session['password'] = password

#获得当前登录的用户
def getUser():
    if 'username' in session:
        return session['username']
    else:
        return None

#检验用户名有效性
def checkUsernameValidity(username):
    #用户名长度不得小于2
    if len(username) < 2:
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


