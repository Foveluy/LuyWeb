import socket
import sys
import time
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
sel = DefaultSelector()
times = 10

class Furture():
    def __init__(self):
        self.coro = None

    def add_coro(self, coro):
        self.coro = coro

    def resume(self):
        global times
        try:
            self.coro.send(None)
        except StopIteration as e:
            times = times - 1


def fetch():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))  # 不会阻塞
    except BlockingIOError as e:
        pass
    f = Furture()

    sel.register(sock.fileno(), EVENT_WRITE, f.resume)
    yield f
    sel.unregister(sock.fileno())

    req = b'GET / HTTP/1.0\r\n Host:www.baidu.com\r\n\r\n'
    sock.send(req)

    sel.register(sock, EVENT_READ, f.resume)
    yield f
    sel.unregister(sock.fileno())
    data = sock.recv(4096)  # Should be ready


def write(conn, mask):
    req = b'GET / HTTP/1.0\r\n Host:www.baidu.com\r\n\r\n'
    sel.unregister(conn)
    conn.send(req)  # Hope it won't block
    sel.register(conn, EVENT_READ, read)


def read(conn, mask):
    data = conn.recv(4096)  # Should be ready
    if data:
        pass
    else:
        global times
        times -= 1
        sel.unregister(conn)


def Task():
    coro = fetch()
    furture = coro.send(None)
    furture.add_coro(coro)


def loop():
    while times:
        events = sel.select()  # 阻塞，有活动连接就返回活动连接列表
        for key, mask in events:
            callback = key.data  # accept
            callback()
            if times <= 0:
                return

if __name__ == '__main__':
    t1 = time.time()
    for i in range(times):
        Task()
    loop()
    t2 = time.time()
    print('耗时:', t2 - t1)
    # 耗时: 0.5629799365997314
