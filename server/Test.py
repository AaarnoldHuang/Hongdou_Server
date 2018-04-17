#! /usr/bin env python3
# -*- coding: utf-8 -*-

from socket import *

HOST = '127.0.0.1'
PORT = 20568
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('Please input: ')
    if not data:
        break
    tcpCliSock.send(data.encode('utf-8'))
    data2 = tcpCliSock.recv(BUFSIZE)
    if not data2:
        break
    print(data2.decode('utf-8'))

tcpCliSock.close()