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
                if data == b'/newUser':
                    tcpCliSock.send('/sure'.encode('utf-8'))
                    userData = tcpCliSock.recv(BUFSIZE)
                    userInfo = userData.decode('utf-8').split(' ')
                    print(userInfo)
                    newuser(userInfo)
                    tcpCliSock.send('/successful'.encode('utf-8'))

                elif data == b'/exit':
                    tcpSerSock.server_close()
                    sys.exit()

                elif data == b'/newTable':
                    newusertable()
                    tcpCliSock.send('/successful'.encode('utf-8'))

                elif data == b'/test':
                    tcpCliSock.send('hi'.encode('utf-8'))

                elif data == b'/check':
                    tcpCliSock.send('Input a name: '.encode('utf-8'))
                    uname = tcpCliSock.recv(BUFSIZE).decode('utf-8')
                    userexitcheck(uname)
                    tcpCliSock.send('ok'.encode('utf-8'))

                elif not data:
                    break
            tcpCliSock.close()
        tcpSerSock.server_close()

def newusertable():
    cursor = mariadb_connection.cursor()
    try:
        cursor.execute("CREATE TABLE hongdou_user (id int primary key, name varchar(20), \
        password varchar(20), sex varchar(6), postNum int)")
    except mariadb.Error as error:
        print("Error: {}".format(error))
    mariadb_connection.commit()
    cursor.close()
    return True

def newdatatable():

    return


def newuser(userinfo):
    cursor = mariadb_connection.cursor()
    try:
        if userexitcheck(userinfo[0]):
            cursor.execute("INSERT INTO hongdou_user (name, password, sex) VALUES \
            (%s, %s, %s)", [userinfo[0], userinfo[1], userinfo[2]])
    except mariadb.Error as error:
        print("Error: {}".format(error))
    mariadb_connection.commit()
    cursor.close()
    return True

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

if __name__ == '__main__':
    HOST = ''
    PORT = 20566
    BUFSIZE = 1024
    mariadb_connection = mariadb.connect(user='hongdou', password='hongdou', database='hongdou_db')
    tcpSerSock = socketserver.ThreadingTCPServer((HOST, PORT), hongdouSocketsServer)
    tcpSerSock.serve_forever()
