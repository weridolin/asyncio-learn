# -*- encoding: utf-8 -*-

## 异步多层回调存在的问题
# 1 多层回调
# def callback_1():
#   # processing ...
#   def callback_2():
#       # processing.....
#       def callback_3():
#           # processing ....
#           def callback_4():
#               #processing .....
#               def callback_5():
#                   # processing ......
#               async_function(callback_5)
#           async_function(callback_4)
#       async_function(callback_3)
#   async_function(callback_2)
# async_function(callback_1)
#
# #
# do_a()
# da_b()
# 如果B处理依赖于a的处理结果，而且A过程时异步调用的，即不知A何时能返回，需要
# 固需将B传给A,让A执行完成后能够去执行B
# do_a(do_b())
#

# 2 共享状态困难
# 如果有需要共享的状态，需要吧每个共享状态都传递给每一个回调，多个异步回调之间共享状态复杂

# 3 错误处理困难
# do_a(do_b(do_c(do_d(do_e(do_f(......))))))
# 上述的 a 到 f。假如 d 抛了异常怎么办？整个调用链断掉，接力传递的状态也会丢失，这种现象称为调用栈撕裂。
# c 不知道该干嘛，继续异常，然后是 b 异常，接着 a 异常。好嘛，报错日志就告诉你，a 调用出错了，但实际是 d 出错。所以，为了防止栈撕裂，异常必须以数据的形式返回，而不是直接抛出异常，然后每个回调中需要检查上次调用的返回值，以防错误吞没。



# 未来对象
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


class Crawler:

    def __init__(self, url):
        self.url = url
        self.response = b""

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)

        try:
            sock.connect(("example.com", 80))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected():
            f.set_Result(None)

        selector.register(sock.fileno(), selectors.EVENT_WRITE, on_connected)
        yield f  # 1
        selector.unregister(sock.fileno())

        get = 'GET{0}HTTP/1.0 \r\n host:example.com'.format(self.url)
        sock.send(get.encode("ascii"))

        global stopped
        while True:
            f = Future()

            def on_readable():
                f.set_Result(sock.recv(4096))

            selector.register(sock.fileno(), selectors.EVENT_READ, on_readable)
            chunk = yield f # 2
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                urls_to.remove(self.url)
                if not urls_to:
                    stopped = True
                break


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


# Task封装了coro对象，即初始化时传递给他的对象，被管理的任务是待执行的协程，
# 故而这里的coro就是fetch()生成器。它还有个step()方法，在初始化的时候就会执行一遍。
# step()内会调用生成器的send()方法，初始化第一次发送的是None就驱动了coro
# 即fetch()的第一次执行 ------>>>> 执行到 1 返回

# send()完成之后，得到下一次的future，然后给下一次的future添加step()回调 # 此时还是在 1 步


# fetch()生成器，其内部写完了所有的业务逻辑，包括如何发送请求，如何读取响应。
# 而且注册给selector的回调相当简单，就是给对应的future对象绑定结果值。
# 两个yield表达式都是返回对应的future对象，然后返回Task.step()之内，
# 这样Task, Future, Coroutine三者精妙地串联在了一起。


# 事件循环驱动 协程从1继续向下运行

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
# 2 Task(crawler.fetch())       # 预激活协程，运行到82行（1处），并对f add_done_Callback函数，同事将事件EVENT_WRITE注册到事件循环
# 3 loop()开始运行，监听EVENT_WRITE事件，触发时，调用on_connected()
# 4 对f set result并执行callback-->即调用TASK.STEP()
# 5 crawler.fetch()继续往下执行，96行继续返回 future 同时已经注册了 READ事件
# 6 loop()继续监听 EVENT_READ事件，触发时调用 ON_READABLE()
# 7 对f set result并执行callback-->即调用TASK.STEP()
# 8 while 里面重复执行直到没有读取到数据完毕，跳出循环，此时 self.core.send(future.result)抛出异常 结束该协程

