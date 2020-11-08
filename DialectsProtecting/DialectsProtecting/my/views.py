# encoding: utf-8

from flask import render_template, request, redirect

from DialectsProtecting.database import db
from DialectsProtecting.my import my
from DialectsProtecting.user.userUtils import uploadFileByCurrentUser, getUser

#用户个人主页
@my.route('/<username>')
def userSpace(username):
    if getUser() == username:
        #进入自己的个人页面
        return render_template('user.html')
    else:
        #进入别人的个人页面，暂定显示404
        return render_template('page404.html')

#上传页面
@my.route('/upload')
def userUpload():
    return render_template('upload.html')

#上传音频界面
@my.route('/uploadform', methods=['POST'])
def uploadAudio():
    #获取数据
    f = request.files['record_file']
    title = request.form['标题']
    translation = request.form['翻译']
    loc = request.form['地域']
    lang = request.form['语言']
    tag1 = request.form['标签1']
    tag2 = request.form['标签2']
    tag3 = request.form['标签3']

    #必要信息为空，表单无效
    if f == None or f.filename == '' or title == '' or lang == '':
        return

    tags = []
    if tag1 != '':
        tags.append(tag1)
    if tag2 != '':
        tags.append(tag2)
    if tag3 != '':
        tags.append(tag3)

    #发布人为当前账户
    publisher = getUser()

    if publisher != None:
        #使用当前账户上传文件到服务器本地
        url = uploadFileByCurrentUser(f)
        #数据库记录此次上传记录
        db.importDialect(
            userName = publisher, 
            audioURL = url, 
            translation = translation, 
            location = loc, 
            language = lang, 
            title = title, 
            tags = tags, 
            like = 0, 
            browse = 0)
        #重定向至上传页面
        return redirect('/my/upload')
    else:
        return render_template('page404.html')