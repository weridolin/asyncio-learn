# -*- encoding: utf-8 -*-
"""
@File           : 异步操作Redis.py
@Time           : 2021/2/17 19:44
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""

# PYTHON 代码操作REDIS时， 链接/操作/断开读视网络IO

import asyncio
import aioredis

async def execute(address,password):
    print("开始执行",address)
    # 网络IO操作，创建REDIS链接
    redis = await aioredis.create_connection(address,password=password)

    # 网络IO操作 在REDIS中设置组键值：CAR,内部再设3个键值对。即redis={
    # car：{key1:1,key2:2,key3:3}}
    # await redis.

