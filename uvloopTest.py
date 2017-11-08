import asyncio
import gc
import os.path
import socket as socket_module
from socket import *
import uvloop
from httptools import HttpRequestParser, HttpParserError

PRINT = 1


class EchoProtocol(asyncio.Protocol):
    def __init__(self):
        self.parser = None
        print(HttpRequestParser(self))

    def connection_made(self, transport):
        self.transport = transport
        if self.parser is None:
            self.parser = HttpRequestParser(self)

    def connection_lost(self, exc):
        self.transport = None

    def data_received(self, data):
        print('recv:收到data',data)
        try:
            self.parser.feed_data(data)
        except HttpParserError as e:
            print('出错', e)
        finally:
            print('进入回调')
            self.transport.write(b'{"b":"fuck"}')

    def on_body(self, body):
        print('parsebody中....')
        print(body)
        print('parse 完毕')


async def echo_server(loop, address, unix):
    if unix:
        sock = socket(AF_UNIX, SOCK_STREAM)
    else:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    if PRINT:
        print('Server listening at', address)
    with sock:
        while True:
            client, addr = await loop.sock_accept(sock)
            if PRINT:
                recv = await loop.sock_recv(client, 10000)
                print('Connection from', addr, 'contain:', recv)
                await loop.sock_sendall(client, recv)


if __name__ == '__main__':

    loop = uvloop.new_event_loop()
    print('using UVLoop')
    asyncio.set_event_loop(loop)
    loop.set_debug(False)
    print('using sock_recv/sock_sendall')

    addr = ('0.0.0.0', 9000)
    coro = loop.create_server(EchoProtocol, *addr)
    # loop.create_task(echo_server(loop, ('0.0.0.0', 5000), False))
    print('Server listening at', addr)
    srv = loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
