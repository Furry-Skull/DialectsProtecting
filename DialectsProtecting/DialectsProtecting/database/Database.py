# encoding: utf-8

#!/usr/bin/python
import sqlite3
from DialectsProtecting.database.Record import Record

class Database:
    def __init__(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            c.execute('''create table user_account
                (account char(16) primary key not null,
                password char(20) not null);''')
        except:
            a="表已存在"

        try:
            c.execute('''create table dialect
                (userName char(16) not null,
                audioURL char(64) primary key not null,
                translation char(64) not null,
                location char(16),
                language char(16),
                title char(16) not null,
                tag char(64),
                like int,
                browse int,
                foreign key(userName) references user_account(account)
                );''')
        except :
            a="数据库已被创建"

        try:
            c.execute('''create table lang
                (language char(16) primary key,
                languageFamily char(16)
                );''')
        except :
            a="数据库已被创建"

        try:
            c.execute('''create table likeURL
                (userName char(16) not null,
                audioURL char(64) not null
                );''')
        except :
            a="数据库已被创建"
        c.close()

    #userName为用户姓名，audioURL为音频路径，translation为译文翻译，暂定支持最大char为64，tags是标签，暂定使用数组的方式
    #返回值为1代表插入数据成功，返回值为0代表插入数据失败（一般原因为audioURL在数据库中已存在，出现了重名，或者是存在非tag值为NULL）
    def importDialect(self, userName, audioURL, translation, location, language, title, tags, like, browse):
        tagStr=''
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        for index in range(len(tags)):
            if index>0:
                tagStr=tagStr+' '+tags[index]
            else :
                tagStr=tags[index]
        try:
            sql_insert = '''
            insert into
                dialect
            values
                (?, ?, ?, ?, ?, ?, ?, 0, 0);
            '''
            c.execute(sql_insert, (userName, audioURL, translation, location, language, title, tagStr))
            conn.commit()
            conn.close()
            return 1
        except:
            conn.close()
            return 0
    
    #插入一种语言的语系
    def insertLanguage(self, languageFamily, language):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            sql_insert = '''
            insert into
                lang
            values
                (?, ?);
            '''
            c.execute(sql_insert, (language,languageFamily))
            conn.commit()
            conn.close()
            return 1
        except:
            conn.close()
            return 0
    

    #点赞功能
    def userLike(self, userName, audioURL):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            sql_insert = '''
            insert into
                likeURL
            values
                (?, ?);
            '''
            c.execute(sql_insert, (userName,audioURL))
            sql_update = '''update dialect set like = like + 1 where audioURL = ?'''
            c.execute(sql_update, (audioURL,))
            conn.commit()
            conn.close()
            return 1
        except:
            conn.close()
            return 0

    #取消用户点赞
    def userDislike(self, userName, audioURL):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            sql_delete = '''delete from likeURL where userName = ? and audioURL = ?'''
            c.execute(sql_delete, (userName,audioURL))
            sql_update = '''update dialect set like = like - 1 where audioURL = ?'''
            c.execute(sql_update, (audioURL,))
            conn.commit()
            conn.close()
            return 1
        except:
            conn.close()
            return 0

    #查询用户是否为此条录音点赞
    def checkLike(self, userName, audioURL):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            sql_select = '''select * from likeURL where userName = ? and audioURL = ?'''
            c.execute(sql_select, (userName,audioURL))
            for row in c:
                conn.close()
                return True
            conn.close()
            return False
        except:
            conn.close()
            return False

    #查询一个账号是否存在，存在返回1，不存在返回0
    def accountExist(self, account):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        sql_select = '''
        select * from user_account where account = ?;
        '''
        c.execute(sql_select,(account,))
        for row in c:
            conn.close()
            return 1
        conn.close()
        return 0

    #查询一个用户已发布的所有方言记录
    def searchUserPublish(self, account):
        return self.__searchDialectPrivate(publishers=[account])
    

    #用户删除一条记录
    def delectDialect(self, audioURL):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        sql_delete = "delete from dialect where audioURL = ?;"
        c.execute(sql_delete,(audioURL,))  
        conn.commit()
        conn.close()
        return 1

    #根据url搜索指定记录
    def searchByURL(self, audioURL):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        sql_select = "select * from dialect where audioURL = ?;"
        c.execute(sql_select,(audioURL,)) 
        for row in c:
            language_Family=self.__lll(row[4])
            row_tag = []
            strlist = row[6].split(' ')
            for value in strlist:
                row_tag.append(value)
            record = Record(userName = row[0], 
                audioURL = row[1], 
                translation = row[2], 
                location = row[3],
                language = row[4],
                title = row[5],
                tags = row_tag,
                like = row[7],
                browse = row[8],
                languageFamily = language_Family
                )
            conn.close()
            return record
        conn.close()
        return None

    #登录代码
    #login返回值为2代表登录成功，返回值为1代表密码错误，返回值为0代表此账号未注册
    def login(self, userName, password):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #conn.execute("alter table user_account add unique key(account)")
        sql_select1 = '''
        select * from user_account where account = ? and password = ?;
        '''
        sql_select2 = '''
        select * from user_account where account = ?;
        '''
        c.execute(sql_select1,(userName, password))        
        for row in c:
            conn.close()
            return 2
        c.execute(sql_select2,(userName,))
        for row in c:
            conn.close()
            return 1
        conn.close()
        return 0


    #注册代码
    #注册失败返回0
    def register(self, userName, password):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        #conn.execute("alter table user_account add unique key(account)")
        try:
            sql_insert = '''
            insert into
                user_account(account,password)
            values
                (?, ?);
            '''
            c.execute(sql_insert, (userName, password))
        except :
            return 0;
        conn.commit()
        conn.close()
        return 1


    def __lll(self, language):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        sql_select1 = '''select languageFamily from lang where language = ?;'''
        c.execute(sql_select1,(language,))  
        for row in c:
            temp = row[0]
            conn.close()
            return temp
        conn.close()

    #根据搜索条件查询记录
    def searchDialect(self, translations=[], languages=[], locations=[], publishers=[], tags=[], languageFamily=[]):
        if len(languageFamily)==0:
            return self.__searchDialectPrivate(translations,languages,locations,publishers,tags)
        else :
            langStr='languageFamily = "'+languageFamily[0]+'"'
            for index in range(len(tags)):
                if index>0:
                    langStr=langStr+'or languageFamily = "'+languageFamily[index]+'"'
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            sql_select1 = '''select language from lang where ''' + langStr + ''';'''
            c.execute(sql_select1)
            for row in c:
                if not row[0] in languages:
                    languages.append(row[0])
            if len(translations)==0 and len(languages)==0 and len(locations)==0 and len(publishers)==0 and len(tags)==0:
                return []
            return self.__searchDialectPrivate(translations,languages,locations,publishers,tags)



    #按照条件搜索方言，返回Record类数组
    def __searchDialectPrivate(self, translations=[], languages=[], locations=[], publishers=[], tags=[]):
        results = []
        #示例创建record的方法
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        if len(tags)>0:
            tagStr="tag like '%"+tags[0]+"%'"
            for index in range(len(tags)):
                if index>0:
                    tagStr=tagStr+"and tag like '%"+tags[index]+"%'"
        else:
            tagStr ="tag like '%%'"

        if len(translations)>0:
            translationStr="translation like '%"+translations[0]+"%'"
            for index in range(len(translations)):
                if index>0:
                    translationStr=translationStr+"and translation like '%"+translations[index]+"%'"
        else:
            translationStr ="translation like '%%'"

        if len(languages)>0:
            languageStr="language like '%"+languages[0]+"%'"
            for index in range(len(languages)):
                if index>0:
                    languageStr=languageStr+"or language like '%"+languages[index]+"%'"
        else:
            languageStr="language like '%%'"

        if len(locations)>0:
            locationStr="location like '%"+locations[0]+"%'"
            for index in range(len(locations)):
                if index>0:
                    locationStr=locationStr+"or location like '%"+locations[index]+"%'"
        else:
            locationStr="location like '%%'"

        if len(publishers)>0:
            publisherStr="userName like '%"+publishers[0]+"%'"
            for index in range(len(publishers)):
                if index>0:
                    publisherStr=publisherStr+"and userName like '%"+publishers[index]+"%'"
        else:
            publisherStr="userName like '%%'"

        sql_select1 = '''
        select * from dialect where (('''+tagStr+''') and ('''+translationStr+''') and ('''+languageStr+''') and ('''+locationStr+''') and ('''+publisherStr+'''));
        '''
        c.execute(sql_select1)  
        for row in c:
            row_tag = []
            strlist = row[6].split(' ')
            for value in strlist:
                row_tag.append(value)
            #sql_select1 = '''select languageFamily from lang where language = row[4];'''
            language_Family=self.__lll(row[4])
            if(language_Family!=None):      
                record = Record(userName = row[0], 
                    audioURL = row[1], 
                    translation = row[2], 
                    location = row[3],
                    language = row[4],
                    title = row[5],
                    tags = row_tag,
                    like = row[7],
                    browse = row[8],
                    languageFamily = language_Family
                    )
                results.append(record)
        return results


    #判断给定字符串是否为一种语系
    def isLanguageFamily(self, languageFamily):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        sql_select = 'select languageFamily from lang where languageFamily = "' + languageFamily + '";'
        c.execute(sql_select)
        for row in c:
            conn.close()
            return True
        conn.close()
        return False

    #判断给定字符串是否为一种语言
    def isLanguage(self, language):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        sql_select = 'select language from lang where language = "' + language + '";'
        c.execute(sql_select)
        for row in c:
            conn.close()
            return True
        conn.close()
        return False

    #获取所有语言，返回数组
    def getAllLanguages(self):
        languages = []
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        sql_select = 'select language from lang;'
        c.execute(sql_select)
        for row in c:
            languages.append(row[0])
        conn.close()
        return languages
