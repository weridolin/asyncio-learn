# -*- encoding: utf-8 -*-
"""
@File           : 异步迭代器.py
@Time           : 2021/2/17 18:29
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""

# 异步可迭代对象：即在 ASYNC FOR语句中可以被使用的对象
# 必须通过他的aiter()返回一个asynchronous iterator
import asyncio

class reader(object):
    """自定义异步可迭代对象"""

    def __init__(self):
        self.count=0

    async def readline(self):
        await asyncio.sleep(2)
        self.count+=1
        if self.count==100:
            return None
        return self.count

    def __aiter__(self):
        return self

    async def __anext__(self):
        val = await self.readline()
        if val==None:
            raise StopAsyncIteration
        return val

async def func():
    obj =reader()
    async for i in obj:
        print(i)

# asyncio.run(func())


class read2():
    def __init__(self):
        self.count=0

    def read(self):
        self.count+=1
        if self.count==20:
            return None
        return self.count

    def __iter__(self):
        return self

    def __next__(self):
        var = self.read()
        if var == None:
            raise StopIteration
        return var

a = read2()
for i in a:
    print(i)
