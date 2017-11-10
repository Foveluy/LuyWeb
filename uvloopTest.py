import asyncio
import gc
import os.path
import socket as socket_module
from socket import *
import uvloop
from httptools import HttpRequestParser, HttpParserError
import functools
from server import LuyProtocol

PRINT = 1

if __name__ == '__main__':

    loop = uvloop.new_event_loop()
    print('using UVLoop')
    asyncio.set_event_loop(loop)
    loop.set_debug(False)
    print('using sock_recv/sock_sendall')

    LuyServer = functools.partial(LuyProtocol, 'fuck')

    addr = ('0.0.0.0', 9000)
    coro = loop.create_server(LuyServer, *addr)
    # loop.create_task(echo_server(loop, ('0.0.0.0', 5000), False))
    print('Server listening at', addr)
    srv = loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
