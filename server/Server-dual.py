#! /usr/bin env python3
# -*- coding: utf-8 -*-

import socketserver
import mysql.connector as mariadb
import json

#新建用户表函数
def newusertable():
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("CREATE TABLE hongdou_user (id int AUTO_INCREMENT, name varchar(20), \
        password varchar(20), sex varchar(6), postNum int, primary key(id))")
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

#登录函数
def login(userinfo):
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("SELECT name, password FROM hongdou_user WHERE \
        name = %s", (userinfo[0],))
        data = cursor.fetchall()
        passwd = data[0]
        print(data)
        if passwd[1] == userinfo[1]:
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    except mariadb.Error as error:
        print("Error: {}".format(error))

#检查用户是否存在函数
def userexitcheck(username):
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("SELECT name FROM hongdou_user WHERE name = %s", (username,))
        if not cursor.fetchall():
            cursor.close()
            return True
        else:
            cursor.close()
            return False
    except mariadb.Error as error:
        print("Error: {}".format(error))

#发布新留言函数
def newMessage(userinfo, message):
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("INSERT INTO hongdou_data (name, anonymous, likes, title, message) \
        VALUES (%s, %s, %s, %s, %s)", (userinfo[0], userinfo[1], 0, userinfo[2], message))
        mariadb_connection.commit()
        cursor.close()
        return True
    except mariadb.Error as error:
        print("Error: {}".format(error))

#返回留言到客户端函数
def getMessages(offset):
    cursor = mariadb_connection.cursor()
    try:
        cmd = "SELECT id, name, anonymous, likes, title FROM \
        hongdou_data LIMIT 10 OFFSET %s" % (offset)
        cursor.execute(cmd)
        messagesdata = cursor.fetchall()
        cursor.close()
        return messagesdata
    except mariadb.Error as error:
        print("Error: {}".format(error))

#返回详细留言函数
def getDetals(id):
    cursor = mariadb_connection.cursor()
    try:
        cmdofGetDetals = "SELECT message FROM hongdou_data WHERE id = %s" % (id)
        cursor.execute(cmdofGetDetals)
        messageDetal = cursor.fetchall()
        cursor.close()
        return messageDetal
    except mariadb.Error as error:
        print("Error: {}".format(error))

#点赞
def liked(id):
    cursor = mariadb_connection.cursor()
    try:
        cmdofLiked = "UPDATE hongdou_data SET likes=likes+1 WHERE id=%s" % (id)
        #cursor.execute("UPDATE hongdou_data SET id=id+1 WHERE id=%s", (id,))
        cursor.execute(cmdofLiked)
        mariadb_connection.commit()
        cursor.close()
        return True
    except mariadb.Error as error:
        print("Error: {}".format(error))

class hongdouSocketsServer(socketserver.BaseRequestHandler):            #不要动

    def handle(self):
        while True:
            tcpCliSock = self.request
            while True:
                data = tcpCliSock.recv(BUFSIZE)
                print(data)
                if data == b'/newUserTable':                                  #新建表函数，CLient中用不到，调试用
                    newusertable()
                    tcpCliSock.send('/success'.encode('utf-8'))

                elif data == b'/newDataTable':
                    if newdatatable():
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('/Failed'.encode('utf-8'))

                elif data == b'/newUser':                                     #当选择创建新用户时
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userSigninInfo = tcpCliSock.recv(BUFSIZE).decode('utf-8').split(' ')        #分割传入信息
                    print(userSigninInfo)                                         #打印分割后的信息
                    if newuser(userSigninInfo):                                   #执行新建用户函数，执行成功给客户端发送/success
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('/Failed. Name existed'.encode('utf-8'))        #执行失败返回信息

                elif data == b'/login':
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userData = tcpCliSock.recv(BUFSIZE)
                    userInfo = userData.decode('utf-8').split(' ')
                    if login(userInfo):
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('/Failed'.encode('utf-8'))

                elif data == b'/newMessage':
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userNewMessgae = tcpCliSock.recv(BUFSIZE).decode('utf-8').split(' ')        #传入格式： 用户名 匿名性 标题
                    print(userNewMessgae)
                    tcpCliSock.send('/GotInfo'.encode('utf-8'))
                    messages = tcpCliSock.recv(BUFSIZE).decode('utf-8')     #确认后传入留言内容
                    print(messages)
                    if newMessage(userNewMessgae, messages):
                        tcpCliSock.send('/success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('Failed'.encode('utf-8'))

                elif data == b'/getMessages':                               #返回首页的10个留言
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userGetMessages = tcpCliSock.recv(BUFSIZE).decode('utf-8')
                    messagesInfo = getMessages(userGetMessages)
                    messagesInfoJson = json.dumps(messagesInfo)
                    print(messagesInfoJson)
                    tcpCliSock.send(messagesInfoJson.encode('utf-8'))

                elif data == b'/getDetals':                                #返回内容详情
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    idOfDetals = tcpCliSock.recv(BUFSIZE).decode('utf-8')
                    messageDetal = json.dumps(getDetals(idOfDetals))
                    print(messageDetal)
                    tcpCliSock.send(messageDetal.encode('utf-8'))

                elif data == b'/liked':
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    idOfLiked = tcpCliSock.recv(BUFSIZE).decode('utf-8')
                    if liked(idOfLiked):
                        tcpCliSock.send('/Success'.encode('utf-8'))
                    else:
                        tcpCliSock.send('/Failed'.encode('utf-8'))

                elif data == b'/test':                                      #测试连接，链接正常返回b'hi'
                    tcpCliSock.send('hi'.encode('utf-8'))

                elif not data:
                    break

                else:
                    tcpCliSock.send('Check ur code plz!'.encode('utf-8'))  #信令输入错误

            tcpCliSock.close()
        tcpSerSock.server_close()


#主函数
if __name__ == '__main__':
    HOST = ''
    PORT = 20566
    BUFSIZE = 1024
    mariadb_connection = mariadb.connect(user='hongdou', password='hongdou', database='hongdou_db')
    tcpSerSock = socketserver.ThreadingTCPServer((HOST, PORT), hongdouSocketsServer)
    tcpSerSock.serve_forever()
