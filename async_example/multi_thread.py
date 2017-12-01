import socket
from concurrent import futures
import time


def sync_way():
    sock = socket.socket()

    sock.connect(('www.baidu.com', 80))  # 阻塞
    req = 'GET / HTTP/1.0\r\n Host:www.baidu.com\r\n\r\n'
    sock.send(req.encode('ascii'))

    rsp = b''
    chunk = sock.recv(4096)
    while chunk:
        rsp += chunk
        chunk = sock.recv(4096) # 我还是阻塞
    return rsp

if __name__ == '__main__':
    t1 = time.time()
    with futures.ThreadPoolExecutor(10) as worker:
        for i in range(100):
            worker.submit(sync_way)

    t2 = time.time()
    print('耗时:', t2 - t1)
    #耗时: 0.605571985244751
