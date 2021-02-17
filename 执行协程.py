# -*- encoding: utf-8 -*-
"""
@File           : 执行协程.py
@Time           : 2021/2/17 11:24
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""
import asyncio

async def func():
    print("?????????")

result = func()

asyncio.run(result)
