#!/usr/bin/python3 
#coding=utf-8 

from socket import * 
import sys 
import getpass

#   getpass  影藏密码输入



def select_logs(s):
    pass

def word_find(s):
    while 1:
        word = input('请输入待查询的单词  输入 ## 退出')

        if word == '##':
            break

        s.send(word.encode())

        data = s.recv(2048)
        if data != b'not find it':
            print(data)

        else:
            print('sorry  this word is not in my hand')

def new_user(s):
    print('开始注册')
    while 1:
        u_name = input('your name')
        password = getpass.getpass('your password')
        passwords = getpass.getpass('password again')


        if (' ' in u_name) or (' ' in password):
            print('不能输入空格')

        if password != passwords:
            print('两次输入不一致') 
            continue

        msg = '%s,%s'%(u_name,password)
        s.send(msg.encode())
        respon = s.recv(1024)
        if respon == b'ok':
            print('注册成功')
            break
        elif respon == b'repeat':
            print('该用户名已存在')
        else:
            pass

def login(s):
    print('开始登录')
    while 1:
        u_name = input('your name')
        password = getpass.getpass('your password')
        if (' ' in u_name) or (' ' in password):
                print('输入错误')
                continue
        msg = u_name + '***' + password

        s.send(msg.encode())

        data = s.recv(1024)

        if data == b'ok':
            print('登录成功')
            
            while 1:
           
                print('1  单词查询  2 查询记录   3 退出')
                user_select = input('请输入')
                s.send(user_select.encode())
                if user_select == '1':
                    word_find(s)
                elif user_select == '2':
                    select_logs(s)
                else:
                    break



        else:
            print('用户名或密码错误')

            ceshi = input('1  重新登录    2  退出')
            if ceshi == '1':
                continue
            else:
                break
        break






#创建网络连接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return 
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return

    while True:
        print('''
            ===========Welcome==========
            -- 1.注册   2.登录    3退出--
            ============================
            ''')
        try:
            cmd = input("输入选项>>")
        except:
            print('命令错误')
            continue

        if cmd not in ['1','2','3']:
            print('请重新输入')
            sys.stdin.flush()
        s.send(cmd.encode())
        if cmd == '1':
            new_user(s)
        if cmd == '2':
            login(s)
        if cmd =='3':
            break


if __name__ == '__main__':
    main()