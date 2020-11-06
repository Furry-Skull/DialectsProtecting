'''单条记录类数据结构'''
class Record:

    #依次传入上传者，音频地址，翻译，地域，语言，标签（标签以数组的方式传入）
    def __init__(self, userName, audioURL, translation, location, language, tags):
        self.publisher = userName
        self.url = audioURL
        self.translation = translation
        self.loc = location
        self.lang = language
        self.tags = tags


