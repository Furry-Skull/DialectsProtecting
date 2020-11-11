# encoding: utf-8
from flask import render_template, request, redirect

from DialectsProtecting.database import db
from DialectsProtecting.my import my
from DialectsProtecting.user.userUtils import checkUserLikeRecords, getUser

#用户个人主页
@my.route('/<username>/space')
def userSpace(username):
    if getUser() == username:
        #进入自己的个人页面，显示个人信息
        return render_template('user.html', 
                               userInfo__userName = '用户名', 
                               userInfo__location = '用户地域', 
                               userInfo__language = '用户语言')
    else:
        #进入别人的个人页面，暂定显示404
        return render_template('page404.html')

#用户收藏夹
@my.route('/<username>/favorite')
def userFavorite(username):
    if getUser() == username:
        #进入收藏夹，需要收藏的records信息
        return render_template('userFavorite.html')
    else:
        #进入别人的个人页面，暂定显示404
        return render_template('page404.html')

#用户上传
@my.route('/<username>/uploaded')
def userUploaded(username):
    if getUser() == username:
        #进入已上传页面，需要上传的records
        myRecords = db.searchUserPublish(username)
        return render_template('userUploaded.html', records = myRecords, likes = checkUserLikeRecords(myRecords))
    else:
        #进入别人的个人页面，暂定显示404
        return render_template('page404.html')

#上传页面
@my.route('/upload')
def userUpload():
    return render_template('upload.html', languageOptions = db.getAllLanguages())

#上传音频界面
@my.route('/uploadform', methods=['POST'])
def uploadAudio():
    #获取数据
    f = request.files['record_file']
    title = request.form['标题']
    translation = request.form['翻译']
    loc = request.form['地域']
    lang = request.form['语言']

    #必要信息为空，表单无效
    if f == None or f.filename == '' or title == '' or lang == '':
        return

    tags = []
    for index in range(0,5):
        tag = request.form.get('标签' + str(index))
        if tag != None and tag != '':
            tags.append(tag)

    #发布人为当前账户
    publisher = getUser()

    if publisher != None:
        #使用当前账户上传文件到服务器本地
        url = uploadFileByCurrentUser(f)
        #数据库记录此次上传记录
        db.importDialect(userName = publisher, 
            audioURL = url, 
            translation = translation, 
            location = loc, 
            language = lang, 
            title = title, 
            tags = tags, 
            like = 0, 
            browse = 0)
        #重定向至我的空间
        return redirect('/my/' + publisher + '/space')
    else:
        return render_template('page404.html')