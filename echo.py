import asyncio
import gc
import os.path
import socket as socket_module
from socket import *
import uvloop

if __name__ == '__main__':
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    except (OSError, NameError):
        pass

    msg = b'fuck' +b'\n'
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
        
