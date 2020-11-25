# encoding: utf-8

from flask import render_template, redirect, request

from DialectsProtecting.database import db
from DialectsProtecting.detail import detail
from DialectsProtecting.config import *
from DialectsProtecting.user.userUtils import getUser

#音频详情展示页面
@detail.route('/' + UPLOAD_PATH + '/<user>/<url>')
def audioDetail(user, url):
    #暂时废弃，直接进入404页面
    return render_template('page404.html')

    audioURL = '/' + UPLOAD_PATH + '/' + user + '/' + url
    record = db.searchByURL(audioURL)
    if record == None:
        return render_template('page404.html')
    return render_template('audioDetail.html', record = record)

#这个函数用于响应点赞的AJAX请求
@detail.route('/like', methods=['POST'])
def like():
    #点赞的音频和用户
    audioURL = request.values.get('audioURL')
    username = getUser()
    if audioURL == None or audioURL == '' or username == None or username == '':
        return render_template('page404.html')

    db.userLike(username, audioURL)
    return ''

#这个函数用于响应取消点赞的AJAX请求
@detail.route('/cancelLike', methods=['POST'])
def cancelLike():
    #点赞的音频和用户
    audioURL = request.values.get('audioURL')
    username = getUser()
    if audioURL == None or audioURL == '' or username == None or username == '':
        return render_template('page404.html')

    db.userCancelLike(username, audioURL)
    return ''

#这个函数用于响应点踩的AJAX请求
@detail.route('/dislike', methods=['POST'])
def dislike():
    #点踩的音频和用户
    audioURL = request.values.get('audioURL')
    username = getUser()
    if audioURL == None or audioURL == '' or username == None or username == '':
        return render_template('page404.html')

    db.userDislike(username, audioURL)
    return ''

#这个函数用于响应取消点踩的AJAX请求
@detail.route('/cancelDislike', methods=['POST'])
def cancelDislike():
    #点踩的音频和用户
    audioURL = request.values.get('audioURL')
    username = getUser()
    if audioURL == None or audioURL == '' or username == None or username == '':
        return render_template('page404.html')

    db.userCancelDislike(username, audioURL)
    return ''