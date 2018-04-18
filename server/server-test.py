#! /usr/bin env python3
# -*- coding: utf-8 -*-

from socket import *
import mysql.connector as mariadb

HOST = ''
PORT = 20566
BUFSIZE = 1024
ADDR = (HOST, PORT)
mariadb_connection = mariadb.connect(user='hongdou', password='hongdou', database='hongdou_db')
#cursor = mariadb_connection.cursor()
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

def newusertable():
    cursor = mariadb_connection.cursor()
    cursor.execute('create table hongdou_testuser (id varchar(10), name varchar(20), \
    password varchar(20), sex varchar(6), postNum int)')
    mariadb_connection.commit()
    cursor.close()
    return

def newuser( id, userinfo):
    cursor = mariadb_connection.cursor()
    cursor.execute('insert into hongdou_testuser (id, name, password, sex) values \
    (%s, %s, %s, %s)', [id, userinfo[0], userinfo[1], userinfo[2]])
    mariadb_connection.commit()
    cursor.close()
    return True

def getId():
    cursor = mariadb_connection.cursor(buffered=True)
    nowid = cursor.execute('select * from hongdou_testuser')
    cursor.close()
    return nowid

while True:
    print('waiting for connecting....')
    tcpCliSock, addr = tcpSerSock.accept()
    print('connected from:', addr)
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        print(data)
        if data == b'/newUser':
            tcpCliSock.send('/sure'.encode('utf-8'))
            userData = tcpCliSock.recv(BUFSIZE)
            userInfo = userData.decode('utf-8').split(' ')
            print(userInfo)
            newuser('00000001', userInfo)
            tcpCliSock.send('/successful'.encode('utf-8'))

        elif data == b'/exit':
            sys.exit()

        elif data == b'/newTable':
            newusertable()
            tcpCliSock.send('/successful'.encode('utf-8'))

        elif data == b'/test':
            tcpCliSock.send('hi'.encode('utf-8'))

        elif not data:
            break
        #tcpCliSock.send(data)
    tcpCliSock.close()
tcpSerSock.close()


