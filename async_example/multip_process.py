import socket
import time
from multiprocessing import Process


def sync_way():
    sock = socket.socket()
    sock.connect(('blog.csdn.net', 80))  # 阻塞
    req = 'GET / HTTP/1.1\r\n Host:blog.csdn.net\r\n\r\n'
    sock.send(req.encode('ascii'))
    rsp = b''
    chunk = sock.recv(4096)

    while chunk:
        rsp += chunk
        chunk = sock.recv(4096)  # 我还是阻塞
        print('收到信息')
    return rsp


if __name__ == '__main__':
    t1 = time.time()
    processes = []
    for i in range(0, 10):
        
        process = Process(target=sync_way)
        process.daemon = True
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
    t2 = time.time()
    print('耗时:', t2 - t1)  # 耗时: 0.6851119995117188
    for process in processes:
        process.terminate()
