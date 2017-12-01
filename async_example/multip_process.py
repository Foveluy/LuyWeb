import socket
import time
from multiprocessing import Process


def sync_way():
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))  # 阻塞
    req = 'GET / HTTP/1.0\r\n Host:www.baidu.com\r\n\r\n'
    sock.send(req.encode('ascii'))
    rsp = b''
    chunk = sock.recv(4096)

    while chunk:
        rsp += chunk
        chunk = sock.recv(4096)  # 我还是阻塞
    return rsp


if __name__ == '__main__':
    t1 = time.time()
    processes = []
    for i in range(0, 100):
        process = Process(target=sync_way)
        process.daemon = True
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
    t2 = time.time()
    print('耗时:', t2 - t1)  # 耗时: 1.0231800079345703
    for process in processes:
        process.terminate()
