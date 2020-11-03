#!/usr/bin/python
import sqlite3


class Database:
    def __init__(self):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        try:
            c.execute('''create table user_account
                (account char(16) primary key not null,
                password char(20) not null);''')
        except :
            a="数据库已被创建"
        c.close()
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

