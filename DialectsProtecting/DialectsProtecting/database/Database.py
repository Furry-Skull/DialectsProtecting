#!/usr/bin/python
import sqlite3
from Record import Record

class Database:
    def __init__(self):
        print (sqlite3.sqlite_version)
        conn = sqlite3.connect('user.db')
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
                tag char(64),
                like int,
                browse int,
                foreign key(userName) references user_account(account)
                );''')
        except :
            a="数据库已被创建"
        
        c.close()

    #userName为用户姓名，audioURL为音频路径，translation为译文翻译，暂定支持最大char为64，tags是标签，暂定使用数组的方式
    #返回值为1代表插入数据成功，返回值为0代表插入数据失败（一般原因为audioURL在数据库中已存在，出现了重名，或者是存在非tag值为NULL）
    def importDialect(self, userName, audioURL, translation, tags):
        tagStr=''
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        for index in range(len(tags)):
            tagStr=tagStr+' '+tags[index]
        try:
            sql_insert = '''
            insert into
                dialect(userName,audioURL,translation,tag,like,browse)
            values
                (?, ?, ?, ?, 0, 0);
            '''
            c.execute(sql_insert, (userName, audioURL, translation, tagStr))
            conn.commit()
            conn.close()
            return 1
        except:
            print ("cn")
            conn.close()
            return 0
    
    #查询一个账号是否存在，存在返回1，不存在返回0
    def accountExist(self, account):
        conn = sqlite3.connect('user.db')
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
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        sql_select = '''
        select * from dialect where userName = ?;
        '''
        c.execute(sql_select,(account,))  
        ret=[]
        for row in c:
            ret.append(row)
        conn.close()
        return ret

    #模糊查询，输入一个字符串，返回所有比对成功的记录
    def fuzzySearch(self, str):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        sql_select = "select * from dialect where translation like '%"+str+"%'"
        c.execute(sql_select)  
        ret=[]
        for row in c:
            ret.append(row)
        conn.close()
        return ret

    #输入方言路径，返回该方言的所有属性
    def getDialectAttribute(self,audioURL):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        sql_select = "select * from dialect where audioURL = ?;"
        c.execute(sql_select,(audioURL,))  
        ret=[]
        for row in c:
            ret.append(row)
        conn.close()
        return ret
    

    #用户删除一条记录
    def delectDialect(self, audioURL):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        sql_delete = "delete from dialect where audioURL = ?;"
        c.execute(sql_delete,(audioURL,))  
        conn.commit()
        conn.close()
        return 1

    #点赞功能是否需要实现？评论功能呢？
    def likeDialect(self, audioURL):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        sql_update = "update dialect set like = like + 1 where audioURL = ?;"
        c.execute(sql_update,(audioURL,))  
        conn.commit()
        conn.close()
        return 1

    #按照tag查询
    #tag格式为xx xx xx xx，通过searchTag函数来查询所有符合该tag的记录,返回值为tuple
    def searchTag(self, tags):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        tagStr="tag like '%"+tags[0]+"%'"
        for index in range(len(tags)):
            if index>0:
                tagStr=tagStr+"and tag like '%"+tags[index]+"%'"
        sql_select1 = '''
        select * from dialect where ('''+tagStr+''');
        '''
        c.execute(sql_select1)  
        ret=[]
        for row in c:
            ret.append(row)
        conn.close()
        return ret


    #登录代码
    #login返回值为2代表登录成功，返回值为1代表密码错误，返回值为0代表此账号未注册
    def login(self, userName, password):
        conn = sqlite3.connect('user.db')
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
        conn = sqlite3.connect('user.db')
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


    #############将这条删除，以下为接口，提供这些接口的实现##############

    #按照条件搜索方言，返回Record类数组
    def searchDialect(self, translations, languages, locations, publishers, tags):
        results = []
        #示例创建record的方法
        record = Record(userName = 'test', 
            audioURL = '/aaa/bbb.mp3', 
            translation = 'testtest', 
            location = 'testloc',
            language = 'lang',
            tags = ['t1', 't2'])
        results.append(record)
        return results

    #判断给定字符串是否为一个地域
    def isLocation(self, location):
        return false

    #判断给定字符串是否为一种语言
    def isLanguage(self, language):
        return false

    #判断给定字符串是否为一个标签
    def isTag(self, tag):
        return false