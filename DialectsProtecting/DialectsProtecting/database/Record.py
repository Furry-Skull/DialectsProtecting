# encoding: utf-8

'''单条记录类数据结构'''
class Record:

    #依次传入上传者，音频地址，翻译，地域，语言，标签（标签以数组的方式传入）
    def __init__(self, userName, audioURL, translation, location, language, title, tags, like, browse, languageFamily):
        self.userName = userName
        self.audioURL = audioURL
        self.translation = translation
        self.location = location
        self.language = language
        self.title = title
        #处理无tag时tag数组存在元素但是字符串为空的情况
        if len(tags) == 1 and tags[0] == '':
            self.tags = []
        else:
            self.tags = tags
        self.like = like
        self.browse = browse
        self.languageFamily = languageFamily


