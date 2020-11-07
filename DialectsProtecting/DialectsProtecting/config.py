# encoding: utf-8

from datetime import timedelta
from os import urandom
import os

from DialectsProtecting import app

#服务器设置
#session有效期为1天
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
#设置秘钥为随机24字节的数
app.config['SECRET_KEY'] = urandom(24)

#用户文件上传的网页中使用的相对地址
UPLOAD_PATH = 'static/uploads'
#用户文件上传的服务器本地地址
LOCAL_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), UPLOAD_PATH)
