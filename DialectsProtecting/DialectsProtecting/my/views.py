from flask import render_template, request, redirect

from DialectsProtecting.database import db
from DialectsProtecting.my import my
from DialectsProtecting.user.userUtils import uploadFileByCurrentUser, getUser

#用户个人主页
@my.route('/<username>')
def userSpace(username):
    if getUser() == username:
        #进入自己的个人页面
        return render_template('testUpload.html')
    else:
        #进入别人的个人页面，暂定显示404
        return render_template('page404.html')

#上传音频界面
@my.route('/upload', methods=['POST'])
def uploadAudio():
    #根据表单name修改
    f = request.files['record_upload']
    user = getUser()
    if user != None:
        #使用当前账户上传文件
        url = uploadFileByCurrentUser(f)
        #数据库记录此次上传记录
        db.importDialect(user, url, '测试翻译', ['测试tag0', '测试tag1'])
        return redirect(getUser())
    else:
        return render_template('page404.html')