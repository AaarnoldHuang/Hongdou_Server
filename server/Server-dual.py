#! /usr/bin env python3
# -*- coding: utf-8 -*-

import socketserver
import mysql.connector as mariadb
import sys

class hongdouSocketsServer(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            tcpCliSock = self.request
            while True:
                data = tcpCliSock.recv(BUFSIZE)
                print(data)
                if data == b'/newUser':                                     #当选择创建新用户时
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userData = tcpCliSock.recv(BUFSIZE)
                    userInfo = userData.decode('utf-8').split(' ')          #分割传入信息
                    print(userInfo)                                         #打印分割后的信息
                    if newuser(userInfo):                                   #执行新建用户函数，执行成功给客户端发送/success
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('/Failed. Name existed'.encode('utf-8'))        #执行失败返回信息

                elif data == b'/newUserTable':                                  #新建表函数，CLient中用不到，调试用
                    newusertable()
                    tcpCliSock.send('/success'.encode('utf-8'))

                elif data == b'/newDataTable':
                    if newdatatable():
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('/Failed'.encode('utf-8'))

                elif data == b'/newMessage':
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userData = tcpCliSock.recv(BUFSIZE)
                    userInfo = userData.decode('utf-8').split(' ')          #传入格式： 用户名 匿名性 标题
                    print(userInfo)
                    tcpCliSock.send('/GotInfo'.encode('utf-8'))
                    messages = tcpCliSock.recv(BUFSIZE).decode('utf-8')     #确认后传入留言内容
                    print(messages)
                    if newMessage(userInfo, messages):
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('Failed'.encode('utf-8'))

                elif data == b'/login':
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userData = tcpCliSock.recv(BUFSIZE)
                    userInfo = userData.decode('utf-8').split(' ')
                    if login(userInfo):
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('/Failed'.encode('utf-8'))

                elif data == b'/test':                                      #测试连接，链接正常返回b'hi'
                    tcpCliSock.send('hi'.encode('utf-8'))

                elif not data:
                    break
            tcpCliSock.close()
        tcpSerSock.server_close()

#新建用户表函数
def newusertable():
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("CREATE TABLE hongdou_user (id int primary key, name varchar(20), \
        password varchar(20), sex varchar(6), postNum int)")
        mariadb_connection.commit()
        cursor.close()
    except mariadb.Error as error:
        print("Error: {}".format(error))
    return True

#新建数据表函数
def newdatatable():
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("CREATE TABLE hongdou_data (id int AUTO_INCREMENT, name varchar(20), \
        anonymous int, likes int, title varchar(100), message varchar(300), primary key(id))")
        mariadb_connection.commit()
        cursor.close()
        return True
    except mariadb.Error as error:
        print("Error: {}".format(error))
    return False

#新建用户函数
def newuser(userinfo):
    cursor = mariadb_connection.cursor()
    try:
        if userexitcheck(userinfo[0]):
            cursor.execute("INSERT INTO hongdou_user (name, password, sex) VALUES \
            (%s, %s, %s)", [userinfo[0], userinfo[1], userinfo[2]])
            mariadb_connection.commit()
            cursor.close()
            return True
        else:
            return False
    except mariadb.Error as error:
        print("Error: {}".format(error))

def login(userinfo):
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("SELECT name, password FROM hongdou_user WHERE \
        name = %s", (userinfo[0],))
        data = cursor.fetchall()
        passwd = data[0]
        print(data)
        if passwd[1] == userinfo[1]:
            return True
        else:
            return False
    except mariadb.Error as error:
        print("Error: {}".format(error))

#检查用户是否存在函数
def userexitcheck(username):
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("SELECT name FROM hongdou_user WHERE name = %s", (username,))
        if not cursor.fetchall():
            return True
        else:
            return False
    except mariadb.Error as error:
        print("Error: {}".format(error))

def newMessage(userinfo, message):
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("INSERT INTO hongdou_data (name, anonymous, likes, title, message) \
        VALUES (%s, %s, %s, %s, %s)", [userinfo[0], userinfo[1], 0, userinfo[2], message])
        mariadb_connection.commit()
        cursor.close()
        return True
    except mariadb.Error as error:
        print("Error: {}".format(error))

#主函数
if __name__ == '__main__':
    HOST = ''
    PORT = 20566
    BUFSIZE = 1024
    mariadb_connection = mariadb.connect(user='hongdou', password='hongdou', database='hongdou_db')
    tcpSerSock = socketserver.ThreadingTCPServer((HOST, PORT), hongdouSocketsServer)
    tcpSerSock.serve_forever()
