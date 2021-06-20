# -*- encoding: utf-8 -*-
"""

"""
import socket
def nonblocking_way():
    sock = socket.socket()
    #！ 设置非阻塞
    sock.setblocking(False)
    try:
        sock.connect(("example.com", 80))
    except BlockingIOError:
        # 非阻塞连接过程会抛出异常
        pass
    request = "GET /HTTP/1.0\r\nHost:example.com\r\n\r\n"
    data =request.encode("utf-8")
    while True:
        # 因为不确定socket何时准备就绪，固不断尝试发送直到send完成
        # 因为connect()已经非阻塞，在send()之时并不知道socket的连接是否就绪，
        # 只有不断尝试，尝试成功为止，即发送数据成功了。recv()调用也是同理。
        try:
            sock.send(data)
            break
        except OSError:
            # SOCKET未准备就绪会抛出这个错误
            pass
    response = b""
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            break
        except OSError:
            # 同样不知道socket何时处于接受状态
            pass
    return response

def sync_way():
    res = []
    for i in range(10):
        print(f"request:: {i}")
        res.append(nonblocking_way())
    return res

if __name__ == '__main__':
    import time
    s = time.perf_counter()
    sync_way()
    e = time.perf_counter() - s
    print(e)


## 1 该版本的非阻塞和同步版本耗费的时间基本差不多，这是因为判断是否准备就绪是在代码里面判断
# 而不是交给OS去判断(代码中两个while)
