#! /usr/bin env python3
# -*- coding: utf-8 -*-

from socket import *
from time import ctime
import mysql.connector as mariadb

HOST = ''
PORT = 20566
BUFSIZE = 1024
ADDR = (HOST, PORT)
mariadb_connection = mariadb.connect(user='hongdou', password='hongdou', database='hongdou_db')

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print('waiting for connecting....')
    tcpCliSock, addr = tcpSerSock.accept()
    print('connected from:', addr)
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        print(data)
        if not data:
            break
        tcpCliSock.send(('[%s] %s'%(ctime(), data)).encode('utf-8'))
    tcpCliSock.close()
tcpSerSock.close()
