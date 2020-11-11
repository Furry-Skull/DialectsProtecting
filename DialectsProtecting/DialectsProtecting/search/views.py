# encoding: utf-8

from flask import render_template, request, redirect

from DialectsProtecting.search import search
from DialectsProtecting.search.searchUtils import *
from DialectsProtecting.user.userUtils import checkUserLikeRecords

#搜索结果请求
@search.route('/', methods=['POST'])
def searchRequest():
    #获取表单数据
    form = request.form
    keywords = form["keywords"]
    #将用户输入的关键词数组转换为搜索表达式
    expr = keywords2expression(keywords)
    #重定向至搜索结果展示页面
    return redirect(expr)

#搜索结果展示页面
@search.route('/<searchExpression>')
def search(searchExpression):
    #执行搜索，返回结果
    records = executeSearch(searchExpression)
    if records == None:
        #表达式错误，返回404页面
        return render_template('page404.html')

    liksses = checkUserLikeRecords(records)
    return render_template('searchResult.html', records = records, likes = checkUserLikeRecords(records))