from flask import render_template, request, redirect, url_for
import os

from DialectsProtecting.my import my

#用户个人主页
@my.route('/<username>')
def userSpace(username):
    return username + '的主页'

#上传音频界面
@my.route('/upload', methods=['GET', 'POST'])
def uploadAudio():
    if request.method == 'POST':
        f = request.files['record_upload']
        #计算服务器本地地址
        basePath = os.path.dirname(__file__)
        uploadPath = os.path.join(basePath, 'uploads', f.filename)
        f.save(uploadPath)
        return redirect(url_for('uploadAudio'))
    elif request.method == 'GET':
        #TODO:访问界面
        return render_template('home.html')