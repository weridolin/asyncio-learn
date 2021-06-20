# -*- encoding: utf-8 -*-

import socket

def blocking_Way():
    sock=socket.socket()
    sock.connect(("example.com",80))
    request = "GET /HTTP/1.0\r\nHost:example.com\r\n\r\n"
    sock.send(request.encode("utf-8"))
    response=b""
    chunk=sock.recv(4096)
    while chunk:
        response+=chunk
        chunk = sock.recv(4096)

    return response


def sync_way():
    res= []
    for i in range(10):
        print(f"request:: {i}")
        res.append(blocking_Way())
    return res

if __name__ == '__main__':
    import time
    s = time.perf_counter()
    sync_way()
    e = time.perf_counter()-s
    print(e)
