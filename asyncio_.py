# -*- encoding: utf-8 -*-
"""
@File           : asyncio_.py
@Time           : 2021/2/16 20:54
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""
import asyncio

@asyncio.coroutine
def func1():
    print(1)
    yield from asyncio.sleep(2) # 遇到耗时IO操作，自动化切换到TASK列表中的其他任务 模拟一次请求
    print(2)

@asyncio.coroutine
def func2():
    print(3)
    yield from asyncio.sleep(2)# 遇到耗时IO操作，自动化切换到TASK列表中的其他任务 模拟一次请求
    print(4)

tasks=[
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

# 协程的启动方式
loop =asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))


### async / await 关键字
import asyncio

async def func1():
    print(1)
    await asyncio.sleep(2) # 遇到耗时IO操作，自动化切换到TASK列表中的其他任务 模拟一次请求
    print(2)

async def func2():
    print(3)
    await asyncio.sleep(2)# 遇到耗时IO操作，自动化切换到TASK列表中的其他任务 模拟一次请求
    print(4)

tasks=[
    asyncio.ensure_future(func1()),
    asyncio.ensure_future(func2())
]

# 协程的启动方式
loop =asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
