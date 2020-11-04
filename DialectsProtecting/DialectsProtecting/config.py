from datetime import timedelta
from os import urandom
import os

from DialectsProtecting import app

#服务器设置
#session有效期为1天
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
#设置秘钥为随机24字节的数
app.config['SECRET_KEY'] = urandom(24)

#用户文件上传文件夹目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')