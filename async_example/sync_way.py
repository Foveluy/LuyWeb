import socket
import time


def sync_way():
    sock = socket.socket()

    sock.connect(('blog.csdn.net', 80))  # 阻塞
    req = 'GET / HTTP/1.0\r\n Host:blog.csdn.net\r\n\r\n'
    sock.send(req.encode('ascii'))

    rsp = b''
    chunk = sock.recv(4096)
    sock.close()
        
    return rsp

if __name__ == '__main__':
    t1 = time.time()
    for i in range(10):
        try:
            sync_way()
        except Exception as e:
            print(e)
    t2 = time.time()

    print('耗时:', t2 - t1)
    #耗时: 6.0183820724487305
