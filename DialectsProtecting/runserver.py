# encoding: utf-8

from os import environ
from DialectsProtecting import app

if __name__ == '__main__':
    #入口函数：启动服务器，本地版本
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

    #服务器版本
    #app.run()