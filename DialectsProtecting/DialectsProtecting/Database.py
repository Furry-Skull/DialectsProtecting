#!/usr/bin/python
import sqlite3

class Database:
    def __init__(self):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        try:
            print ("cnmd")
            c.execute('''create table user_account
                (account char(16) primary key not null,
                password char(20) not null);''')
        except:
            print("表已存在")

        try:
            c.execute('''create table dialect
                (userName char(16) not null,
                audioURL char(64) primary key not null,
                translation char(64) not null,
                tag char(64),
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
                dialect(userName,audioURL,translation,tag)
            values
                (?, ?, ?, ?);
            '''
            c.execute(sql_insert, (userName, audioURL, translation, tagStr))
            conn.commit()
            conn.close()
            return 1
        except:
            print ("cn")
            conn.close()
            return 0


    #tag格式为xx xx xx xx，通过searchTag函数来查询所有符合该tag的记录,返回值为tuple
    def searchTag(self, tags):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        tagStr="tag like '%"+tags[0]+"%'"
        for index in range(len(tags)):
            if index>0:
                tagStr=tagStr+"and tag like '%tags[index]%'"
        sql_select1 = '''
        select * from dialect where ('''+tagStr+''');
        '''
        c.execute(sql_select1)  
        ret=[]
        for row in c:
            ret.append(row)
        conn.close()
        return ret


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
    #创建失败返回0
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

