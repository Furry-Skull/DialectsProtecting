# encoding: utf-8

#用户相关操作，主要管理session

from flask import session
import os
import time

from DialectsProtecting.config import UPLOAD_PATH, LOCAL_UPLOAD_PATH
from DialectsProtecting.database import db

#登录账户，在session留下记录
def sessionLogin(username, password):
    session['username'] = username
    session['password'] = password

#登出账户，清除session记录
def sessionLogout():
    session.pop('username', None)

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

#使用当前登录的账户上传文件，并返回存储地址（相对路径）
def uploadFileByCurrentUser(file):
    if 'username' in session:
        #计算服务器上传文件夹的地址
        uploadFolderPath = os.path.join(LOCAL_UPLOAD_PATH, session['username'])
        #创建必要的文件夹
        if not os.path.exists(uploadFolderPath):
            os.makedirs(uploadFolderPath)
        #获取当前服务器时间作为文件名前缀，保证不会重名
        timestr = str(int(round(time.time() * 1000)))

        #服务器本地地址
        localPath = os.path.join(LOCAL_UPLOAD_PATH, session['username'], timestr + '-' + file.filename)
        file.save(localPath)
        #相对地址
        uploadPath = '/' + UPLOAD_PATH + '/' + session['username'] + '/' + timestr + '-' + file.filename
        return uploadPath

#输入音频记录数组，生成与records对应的，记录该用户是否给对应索引的音频点赞的数组
def checkUserLikeRecords(records):
    username = getUser()
    isUserLikes = [] #与records对应的，记录该用户是否给对应索引的音频点赞
    if username != None:
        for item in records:
            if db.checkLike(userName = username, audioURL = item.audioURL):
                isUserLikes.append(True)
            else:
                isUserLikes.append(False)
        return isUserLikes
    return []