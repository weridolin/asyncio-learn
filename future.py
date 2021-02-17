# -*- encoding: utf-8 -*-
"""
@File           : future.py
@Time           : 2021/2/17 12:36
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""

# future:task 继承future，TASK对象内部AWAIT结果的处理基于FUTURE对象来的

import asyncio
## demo1
async def main():
    # 获取当前事件循环
    loop = asyncio.get_running_loop()

    # 创建一个任务（FUTURE对象），这个任务什么都不干
    FUT = loop.create_future()

    # 等待任务最终结果，没结果会一直等下去
    await FUT

# asyncio.run(main())


# DEMO2
import asyncio
async def set_after(fut:asyncio.Future):
    await asyncio.sleep(2)
    fut.set_result("end")

async def main():
    # 获取当前事件循环
    loop = asyncio.get_running_loop()

    # 创建一个任务（FUTURE对象），这个任务什么都不干
    FUT = loop.create_future()

    # 创建一个任务（TASK对象），绑定SET_RESULT函数，函数在2S后，会被FUT赋值
    # 即手动设置FUTURE任务的最终结果，FUT即可结束
    await loop.create_task(set_after(fut=FUT))

    # 等待任务最终结果，没结果会一直等下去
    R = await FUT
    print(R)
asyncio.run(main())

###### 固创建TASK时其实就绑定了FUT,即函数的返回值为FUT
