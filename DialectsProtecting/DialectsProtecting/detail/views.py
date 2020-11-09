# encoding: utf-8

from flask import render_template, redirect

from DialectsProtecting.database import db
from DialectsProtecting.detail import detail
from DialectsProtecting.config import *

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