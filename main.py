#!/usr/bin/env python3
#coding:utf-8
from __future__ import print_function
import socket

HOST, PORT = '', 8080


def main():
    listen_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_Sock.bind((HOST, PORT))
    listen_Sock.listen(1)
    print('LuyWeb listen on port %s ...' % PORT)
    while True:
        client_con, client_addr = listen_Sock.accept()
        request = client_con.recv(1024)
        print(client_addr, 'connected')
        http_response = """\
HTTP/1.1 200 OK
Content-Type:text/html
\r\n

Hello, World!
"""
        # sendall() 需要字节型字符串，因此http_response 需要切换字符
        print('returning:',http_response)
        client_con.sendall(http_response.encode(encoding='utf_8'))
        client_con.close()


if __name__ == '__main__':
    main()
