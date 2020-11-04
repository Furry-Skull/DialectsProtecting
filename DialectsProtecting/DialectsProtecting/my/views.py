from flask import render_template, request, redirect, url_for


from DialectsProtecting.my import my
from DialectsProtecting.user.userUtils import uploadFileByCurrentUser, getUser

#用户个人主页
@my.route('/<username>')
def userSpace(username):
    return username + '的主页'

#上传音频界面
@my.route('/upload', methods=['POST'])
def uploadAudio():
    f = request.files['record_upload']
    #使用当前账户上传文件
    uploadFileByCurrentUser(f)
    if getUser() != None:
        return redirect(getUser())
    else:
        return render_template('page404.html')