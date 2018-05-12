#! /usr/bin env python3
# -*- coding: utf-8 -*-

from socket import *

HOST = '45.63.91.170'
PORT = 20566
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('Please input: ')
    if not data:
        break
    tcpCliSock.send(data.encode('utf-8'))
    data2 = tcpCliSock.recv(BUFSIZE).decode('utf-8')
    if not data2:
        break
    print(data2)
tcpCliSock.close()