import socket
import time


def sync_way():
    sock = socket.socket()

    sock.connect(('blog.csdn.net', 80))  # 阻塞
    req = 'GET / HTTP/1.1\r\n Host:blog.csdn.net\r\n\r\n'
    sock.send(req.encode('ascii'))

    rsp = b''
    chunk = sock.recv(4096)
    while chunk:
        rsp += chunk
        chunk = sock.recv(4096) # 我还是阻塞
        
    return rsp

if __name__ == '__main__':
    t1 = time.time()
    for i in range(10):
        sync_way()
    t2 = time.time()

    print('耗时:', t2 - t1)
    #耗时: 5.692497968673706
