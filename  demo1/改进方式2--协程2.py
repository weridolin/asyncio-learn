# -*- encoding: utf-8 -*-



import socket
import selectors

selector = selectors.DefaultSelector()
stopped = False
urls_to = ['/', '/1', '/2', '/3', '/4', '/5', '/6', '/7']


class Future:
    def __init__(self):
        self.result = None
        self._callback = []

    def add_done_Callback(self, fn):
        self._callback.append(fn)

    def set_Result(self, result):
        self.result = result
        for fn in self._callback:
            fn(self)

    def __iter__(self):
        yield self
        return self.result

def connect(sock,address):
    sock.setblocking(False)
    f = Future()
    try:
        sock.connect(address)
    except BlockingIOError:
        pass

    def on_connected():
        f.set_Result(None)
    selector.register(sock.fileno(), selectors.EVENT_WRITE, on_connected)
    yield from f  # 1
    selector.unregister(sock.fileno())

def read(sock):
    f = Future()

    def on_readable():
        f.set_Result(sock.recv(4096))

    selector.register(sock.fileno(), selectors.EVENT_READ, on_readable)
    chunk = yield from f  # 2
    selector.unregister(sock.fileno())
    return chunk

def read_All(sock):
    response=[]
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)

    return b"".join(response)

class Crawler:

    def __init__(self, url):
        self.url = url
        self.response = b""

    def fetch(self):
        sock = socket.socket()
        yield from connect(sock,("example.com",80))
        get = 'GET{0}HTTP/1.0 \r\n host:example.com'.format(self.url)
        sock.send(get.encode("ascii"))
        global stopped
        self.response=yield from read_All(sock)
        urls_to.remove(self.url)
        if not urls_to:
            stopped = True


class Task:
    def __init__(self, core):
        self.core = core
        f = Future()
        f.set_Result(None)
        self.step(f)

    def step(self, future: Future):
        try:
            # send 会进入到core执行 即fetch 直到下次yield
            # next future 未yield返回的对象
            next_future = self.core.send(future.result)
        except StopIteration:
            return
        next_future.add_done_Callback(self.step)  # add_done_callback()不是给写爬虫业务逻辑用的。



def loop():
    while not stopped:
        # 阻塞直到事件发生
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()


if __name__ == '__main__':
    import time

    s = time.time()
    for url in urls_to:
        crawler = Crawler(url=url)
        Task(crawler.fetch()) # crawler.fetch()执行到1
    loop()
    print(time.time() - s)

# 执行流程
# 1 crawler = Crawler(url=url)  # 初始化未协程，此时还未预激活
# 2 Task(crawler.fetch())       # 预激活协程，运行到42行（1）返回
# 3 loop()开始运行，监听EVENT_WRITE事件，触发时，调用on_connected()
# 4 对f set result并执行callback-->即调用TASK.STEP()
# 5 connect 从42继续往下执行，返回 crawler执行到76行
# 6 loop()继续监听 EVENT_READ事件，触发时调用 ON_READABLE()
# 7 对f set result并执行callback-->即调用TASK.STEP()
# 8 while 里面重复执行直到没有读取到数据完毕，跳出循环，此时 self.core.send(future.result)抛出异常 结束该协程

