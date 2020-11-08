# encoding: utf-8

'''搜索表达式的翻译，分割和执行'''

'''
搜索表达式，形式为
translation=aaa&lang=xx&langFamily=ttt&loc=yy&publisher=ddd&tag=bb&tag=cc
对于lang, loc, publisher（语言，地区和发布者）各自来说，有多个条件意味着多选，是或的关系
对于translation和tag来说，多个条件是与的关系
不同key表达式之间都是与的关系
&符号将各表达式联合在一起
'''

from DialectsProtecting.database import db


#将以空格分割的关键词组字符串翻译为字符串搜索表达式
def keywords2expression(keywords):
    #按照空格分割
    keywordsArray = keywords.split(' ')

    expr = ''

    for index, keyword in enumerate(keywordsArray):
        if db.isLanguage(keyword):
            expr += 'lang=' + keyword
        elif db.isLanguageFamily(keyword):
            expr += 'langFamily=' + keyword
        else:
            #其他关键词会被视为翻译
            expr += 'translation=' + keyword

        if index < len(keywordsArray) - 1:
            #不为最后一个关键词
            expr += '&'

    return expr


#将字符串搜索表达式分割为多个单独的搜索条件并交给数据库执行，返回Record类数组，如果返回None表示表达式错误
#返回空数组和返回None意义不一样，前者表示无搜索结果
def executeSearch(expr):
    searchTranslations = []
    searchLangs = []
    searchLangFamilies = []
    searchLoc = []
    searchPublishers = []
    searchTags = []

    expressions = expr.split('&')
    #按&分割
    if not len(expressions) > 0:
        return None
    for item in expressions:
        #按=分割，itemSplit有且仅有左边的值key和右边的值value
        itemSplit = item.split('=')
        if len(itemSplit) != 2:
            return None
        else:
            key = itemSplit[0]
            value = itemSplit[1]
            if key == 'translation':
                searchTranslations.append(value)
            elif key == 'lang':
                searchLangs.append(value)
            elif key == 'langFamily':
                searchLangFamilies.append(value)
            elif key == 'loc':
                searchLoc.append(value)
            elif key == 'publisher':
                searchPublishers.append(value)
            elif key == 'tag':
                searchTags.append(value)
            else:
                #无匹配项，返回None
                return None

    #返回搜索结果
    return db.searchDialect(
        translations = searchTranslations, 
        languages = searchLangs, 
        languageFamily = searchLangFamilies,
        locations = searchLoc, 
        publishers = searchPublishers, 
        tags = searchTags)