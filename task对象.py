# -*- encoding: utf-8 -*-
"""
@File           : task对象.py
@Time           : 2021/2/17 11:57
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""

# task:在事件循环中添加任务
# tasks用于并发调度协程，通过ASYNCIO.CREATE_TASK（协程对象）的方式
# 创建TASK对象，这样可以让携程加入事件循环中等待被调度执行，还可以使用
# LOOP.CREATE_TASK()或ENSURE_FUTURE函数
import asyncio
async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"

async def func():
    print("开始执行协程函数")
    # 创建TASK对象，添加到事件循环
    task1 = asyncio.create_task(others())
    task2 = asyncio.create_task(others())

    res1 = await task1
    print("IO请求结束",res1)
    res2 = await task2
    print("IO请求结束",res2)
asyncio.run(func())

import asyncio
async def others():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"

async def func():
    print("开始执行协程函数")
    # 创建TASK对象，添加到事件循环
    task_list=[
        asyncio.create_task(others()),
        asyncio.create_task(others())
    ]

    done= await asyncio.wait(task_list,timeout=None)
    print(done)
asyncio.run(func())
