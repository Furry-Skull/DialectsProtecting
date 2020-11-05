from flask import render_template, request, redirect

from DialectsProtecting.database import db
from DialectsProtecting.search import search

#搜索结果请求
@search.route('/', methods=['POST'])
def searchRequest():
    #获取表单数据
    form = request.form
    expression = form["expression"]
    #重定向至搜索结果展示页面
    return redirect(expression)

#搜索结果展示页面
@search.route('/<searchExpression>')
def search(searchExpression):
    '''
    搜索表达式，形式为
    translation=aaa&lang=xx&loc=yy&publisher=ddd&tag=bb&tag=cc
    对于lang, loc, publisher（语言，地区和发布者）各自来说，有多个条件意味着多选，是或的关系
    对于translation和tag来说，多个条件是与的关系
    不同key表达式之间都是与的关系
    &符号将各表达式联合在一起
    '''

    searchTranslations = []
    searchLangs = []
    searchLoc = []
    searchPublishers = []
    searchTags = []

    expressions = searchExpression.split('&')
    #按&分割
    if not len(expressions) > 0:
        return render_template('page404.html')
    for item in expressions:
        #按=分割，itemSplit有且仅有左边的值key和右边的值value
        itemSplit = item.split('=')
        if len(itemSplit) != 2:
            return render_template('page404.html')
        else:
            key = itemSplit[0]
            value = itemSplit[1]
            if key == 'translation':
                searchTranslations.append(value)
            elif key == 'lang':
                searchLangs.append(value)
            elif key == 'loc':
                searchLoc.append(value)
            elif key == 'publisher':
                searchPublishers.append(value)
            elif key == 'tag':
                searchTags.append(value)
            else:
                #无匹配项，返回404
                return render_template('page404.html')

    return searchExpression;