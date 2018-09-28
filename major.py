from socket import *

import os

import signal
from pymysql import connect

import sys

#   user:uname ,password    mydict    logs

conn = connect(host='127.0.0.1', user='test', password='123456',
               database='all_dict', charset='utf8', port=3306)

cur = conn.cursor()


sql_newuser = 'insert into user(uname,password) values(%s,%s)'


def my_find(c,id):
    while 1:
        word = c.recv(1024).decode()

        if word == b'##':
            break
        sql_word = 'select word_value from mydict where word="%s"'%(word)
        print(sql_word)
        cur.execute(sql_word)
        row = cur.fetchone()
        if row:
            c.send(row[0].encode())

            sql_ins = 'insert into logs(uid,recodes) values (%s,%s)'

            cur.execute(sql_ins,(id,word+': '+row[0]))
            conn.commit()
            print('已添加')

        else:
            print('没找到')
            c.send(b'not find it')


def login(c):
    print('等待接受用户名')
    new_name_password = c.recv(1024)
    if not new_name_password :
        return
    new_name_password=str(new_name_password.decode()).split('***')
    u_name = new_name_password[0]
    password = new_name_password[1]
    sql_select = "select * from user where uname='%s'and password='%s'"%(u_name,password)
    print(sql_select)
    cur.execute(sql_select)
    rows = cur.fetchone()

    if rows:
        print('登录成功')
        c.send(b'ok')
        print(rows)
        while 1:
           
            
            user_select = c.recv(1024)
            if user_select == b'1':
                my_find(c,rows[0])
            elif user_select == b'2':
                select_logs(rows[0])
            else:
                print('woshi break')
                break
    else :
        c.send(b'erro')


def new_user(c):
    new_name_password = c.recv(1024)
    if not new_name_password :
        return
    new_name_password=str(new_name_password.decode()).split(',')
    u_name = new_name_password[0]
    password = new_name_password[1]
    sql_select = 'select * from user where uname=%s'
    cur.execute(sql_select,u_name)
    rows = cur.fetchone()

    if rows is None:
        cur.execute(sql_newuser,(u_name,password))
        conn.commit()
        c.send(b'ok')
        print('添加成功')



    else:
        c.send(b'repeat')


def do_child(c):
    while 1:
        data = c.recv(1024)
        if (not data) or data == '3':
            sys.exit('子进程退出')
        print(data)
        if data == b'1':
            print('注册程序')
            new_user(c)

        elif data == b'2':
            print('登录程序')
            login(c)


def main(s):
    while 1:
        try:
            c, addr = s.accept()
        except KeyboardInterrupt as e:
            sys.exit('程序结束')
         # 忽略子进程信号

        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

        pid = os.fork()

        if pid < 0:
            print('子进程创建失败,程序结束')
            sys.exit('程序结束')
        elif pid == 0:
            print('子进程')

            s.close()

            do_child(c)

            sys.exit('子进程结束')
        else:
            print('父进程')

            c.close()


if __name__ == '__main__':
    s = socket()

    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    s.bind(('127.0.0.1', 4399))

    s.listen(5)

    main(s)
