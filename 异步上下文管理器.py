# -*- encoding: utf-8 -*-
"""
@File           : 异步上下文管理器.py
@Time           : 2021/2/17 18:42
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""
# async with ：通过定义__aenter__()和__aexit()__来定义
import asyncio
class AsyncContextManager:
    def __init__(self):
        self.conn=None

    async def do_Sth(self):
        # op database
        return "op end"
    

    async def __aenter__(self):
        # 异步链接到数据库
        self.conn=await asyncio.sleep(1)
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 异步关闭数据库
        await asyncio.sleep(1)

async def func():
    async with AsyncContextManager() as f:
        res = await f.do_Sth()
        print(res)

asyncio.run(func())
