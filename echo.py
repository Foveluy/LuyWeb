import asyncio
import gc
import os.path
import socket as socket_module
from socket import *
import uvloop

import functools


class shit:
    def __init__(self, fuck='default'):
        self.fuck = fuck

    def Print(self):
        print(self.fuck)


def makeShit(shit):  # 注意这里传递的参数是shit这个类
    shitIns = shit()
    shitIns.Print()


if __name__ == '__main__':
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    except (OSError, NameError):
        pass

    makeShit(shit)

    newShit = functools.partial(shit, 'fuck')

    makeShit(newShit)  # 此时输出 fuck

    msg = b'fuck' + b'\n'
    msgLength = len(msg)

    sock.connect(('0.0.0.0', 8080))
    sock.sendall(msg)
    nrecv = 0
    while nrecv < msgLength:
        resp = sock.recv(msgLength)
        print('recv from server:', resp)
        if not resp:
            raise SystemExit()
        nrecv += len(resp)
