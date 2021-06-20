# -*- encoding: utf-8 -*-

# 1  io、阻塞的时候，将运行的权利交出去，当阻塞事件完成的时候，
# 2  通过一个回调来唤醒程序继续往下走，并且返回io事件的值
import asyncio


class Future:
    _FINISHED = 'finished'
    _PENDING = 'pending'
    _CANCELLED = 'CANCELLED'

    def __init__(self, loop=None):
        if loop is None:
            self._loop = get_event_loop() # 获取当前的 eventloop
        else:
            self._loop = loop
        self._callbacks = []
        self.status = self._PENDING
        self._blocking = False
        self._result = None

    def _schedule_callbacks(self):
        # 将回调函数添加到事件队列里，eventloop 稍后会运行
        for callbacks in self._callbacks:
            self._loop.add_ready(callbacks)
        self._callbacks = []

    def add_done_callback(self, callback, *args):
        # 为 future 增加回调函数
        if self.done():
            self._loop.call_soon(callback, *args)
        else:
            handle = Handle(callback, self._loop, *args)
            self._callbacks.append(handle)

    def set_result(self, result):
        # 给future设置结果，并将 future 置为结束状态
        self.status = self._FINISHED
        self._result = result

    def done(self):
        return self.status != self._PENDING

    def result(self):
        # 获取future 的结果
        if self.status != self._FINISHED:
            raise AttributeError('future is not ready')
        return self._result

    def __iter__(self):
        # 第一次启动的时候，将自身设置为
        # 阻塞状态，然后返回self 。暴露出
        # set_result方法让回调函数可以给
        # future设置返回值，并且将
        # future更改为结束状态
        if not self.done():
            self._blocking = True
        yield self  # 返回自身
        assert self.done(), 'future not done'  # 下一次运行 future 的时候，要确定 future 对应的事件已经运行完毕
        return self.result()

        # coro 通过 coro.send(None) 启动，遇到 io 操作，
        # 会用 yield 返回一个 future。io 操作完成之后，
        # 回调函数通过 coro.send(None) 继续往下进行。直到 coro.send(None) 爆出 StopIteration 异常
        # 协程运行完毕。


class Handle:

    def __init__(self, callback, loop, *args):
        self._callback = callback
        self._args = args

    def _run(self):
        self._callback(*self._args)


import collections


class EventloopError(Exception): pass


# 时间循环

# 事件驱动模式，就是有一个队列，里面存放着一堆函数，从第一个函数开始执行，
# 在函数执行的过程中，可能会有新的函数继续加入到这个队列中。一直到队列中所有的函数被执行完毕，并且再也不会有新的函数被添加到这个队列中。
#
# 协程非常适合这种模式，协程的启动就是将 coro.send(None) 加入到 eventloop 的队列中。
# future 回调完成之后，再将 coro.send(None) 加入到队列中就可以驱使协程继续往下走。
class Eventloop:

    def __init__(self):
        self._ready = collections.deque()  # 事件队列
        self._stopping = False

    def stop(self):
        self._stopping = True

    def call_soon(self, callback, *args):
        # 将事件添加到队列里
        handle = Handle(callback, self, *args)
        self._ready.append(handle)

    def add_ready(self, handle):
        # 将事件添加到队列里
        if isinstance(handle, Handle):
            self._ready.append(handle)
        else:
            raise EventloopError('only handle is allowed to join in ready')

    def run_once(self):
        # 执行队列里的事件
        ntodo = len(self._ready)
        for i in range(ntodo):
            handle = self._ready.popleft()
            handle._run()

    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break

# 协程的推动需要将 coro.send(None) 添加到 eventloop 里，
# 所以将 eventloop 设置为一个全局变量，用一个函数来获取他。
_event_loop = None


def get_event_loop():
    global _event_loop
    if _event_loop is None:
        _event_loop = Eventloop()
    return _event_loop


class Task(Future):

    def __init__(self, coro, loop=None):
        super().__init__(loop=loop)
        self._coro = coro    # 协程
        self._loop.call_soon(self._step) # 预激活协程，将_step添加到EVENT_LOOP事件循环里面.

    def _step(self, exc=None):
        try:
            if exc is None:
                result = self._coro.send(None)
            else:
                result = self._coro.throw(exc)   # 有异常，则抛出异常
        except StopIteration as exc:   # 说明协程已经执行完毕，为协程设置值
            self.set_result(exc.value)
        else:
            if isinstance(result, Future):
                if result._blocking:
                    self._blocking = False
                    result.add_done_callback(self._wakeup, result)
                else:
                    self._loop.call_soon(
                        self._step, RuntimeError('你是不是用了 yield 才导致这个error?')
                    )
            elif result is None:
                self._loop.call_soon(self._step)
            else:
                self._loop.call_soon(self._step, RuntimeError('你产生了一个不合规范的值'))

    def _wakeup(self, future):
        try:
            future.result()  # 查看future 运行是否有异常
        except Exception as exc:
            self._step(exc)
        else:
            self._step()

# task 的 _coro 就是协程。task只有两个方法。_step 实际上就是执行 _coro.send(None)，
# 根据协程的产出值来进行下一步。当返回了一个 future，如果是阻塞中的状态 _blocking ，
# 就将唤醒自己作为 future 的回调函数。future 回调完毕之后，就会唤醒协程进行下一步。
# 如果产出一个 None，那么就无须阻塞，继续往下进行。将self._step 添加到 eventloop 的事件队列里。等待 eventloop 稍后执行。


