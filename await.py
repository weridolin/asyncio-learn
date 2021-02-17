# -*- encoding: utf-8 -*-
"""
@File           : await.py
@Time           : 2021/2/17 11:26
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""

# await
# await 可等待的对象：（协程对象 future task对象）=》IO等待
import asyncio
async def func():
    print("aaaaaaaaaaa")
    res = await asyncio.sleep(2) #IO等待 等到返回结果才往下执行
    print("结束",res)

asyncio.run(func())

async def others():
    print("????")
    await asyncio.sleep(2)
    print("end")
    return "返回值"

async def func():
    print("开始执行协程函数")

    res1 = await others()
    print("IO请求结束",res1)

    res2 = await others()
    print("IO请求结束",res2)
asyncio.run(func())


## 多个await


