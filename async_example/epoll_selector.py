import socket
import sys
import time
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

sel = DefaultSelector()

times = 100


def read(conn, mask):
    data = conn.recv(4096)  # Should be ready
    if data:
        pass
    else:
        global times
        times -= 1
        sel.unregister(conn)

def write(conn, mask):
    req = b'GET / HTTP/1.0\r\n Host:www.baidu.com\r\n\r\n'
    sel.unregister(conn)
    conn.send(req)  # Hope it won't block
    sel.register(conn, EVENT_READ, read)


def fetch():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))  # 阻塞
    except BlockingIOError as e:
        pass

    sel.register(sock, EVENT_WRITE, write)


def sync_way():
    while times:
        events = sel.select()  # m默认阻塞，有活动连接就返回活动连接列表
        for key, mask in events:
            callback = key.data  # accept
            callback(key.fileobj, mask)


if __name__ == '__main__':
    t1 = time.time()
    for i in range(times):
        fetch()
    sync_way()
    t2 = time.time()
    print('耗时:', t2 - t1)
    #耗时: 0.9249680042266846