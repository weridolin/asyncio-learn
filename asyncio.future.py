# -*- encoding: utf-8 -*-
"""
@File           : asyncio.future.py
@Time           : 2021/2/17 14:44
@Author         : 林宏基
@Email          : 359066432@qq.com
@Software       : PyCharm
@Description    :
"""

# concurrent.futures.future对象： 使用线程池，进程池实现异步操作时用到的对象
import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor

def func(v):
    time.sleep(2)
    print(v)
    return "End"

# 创建线程池
pool =ThreadPoolExecutor(max_workers=5)

# for i in range(10):
#     fut = pool.submit(func,i)
#     print(fut)


def fun1():
    # 某个具体耗时操作
    time.sleep(2)
    return "end"
import asyncio
async def main():
    loop = asyncio.get_running_loop()
    # 1 run in the default loop's executor(默认ThreadPoolExecutor)
    # 第一步：内部会先调用默认ThreadPoolExecutor的submit去线程池中申请一个线程
    # 去执行fun1函数，返回一个concurrent.futures.Future对象
    # 第二步：调用asyncio.wrap_future将concurrent.futures.Future对象包装为asyncio.FUTURE对象
    # 因为concurrent.futures.Future对象不支持AWAIT语法，固要包装为asyncio.FUTURE对象才能使用
    fut = loop.run_in_executor(None,fun1)
    result = await fut
    print("Default thread pool",result)

    # 2 run in a custom thread pool:
    # with concurrent.futures.ThreadPoolExecutor() as pool:
    #     result=await loop.run_in_executor(pool,fun1)
    #     print("custom thread pool",result)

    # 3 run in a custom process pool:
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result=await loop.run_in_executor(pool,fun1)
    #     print("custom process pool",result)
# asyncio.run(main())


# asyncio+不支持异步的模块
import requests

async def download_image(url:str):
    print("开始下载",url)
    loop = asyncio.get_event_loop()

    # requests模块不支持异步操作，所以使用线程池在配合实现了
    future = loop.run_in_executor(None,requests.get,url)

    res = await future
    # 图片保存本地文件
    filename = url[40:50]+'.jpg'
    with open(filename,mode="wb") as file_object:
        file_object.write(res.content)

if __name__ == '__main__':
    urlist=[
        "https://th.bing.com/th/id/Rf27c1a2fe19310a12b595063e8a57e17?rik=gM7Zu1QoOaSTmQ&riu=http%3a%2f%2fwww.dnzhuti.com%2fuploads%2fallimg%2f161230%2f95-161230160H0.jpg&ehk=R9HqrAVAoWSdhWbxLlCAldyrM1EY4Ho5%2faPMEUP5aYE%3d&risl=&pid=ImgRaw",
        "https://th.bing.com/th/id/Rc2c19809bf2fe6394a76b2e7d9ec156d?rik=2kVroExkhAd%2bpw&riu=http%3a%2f%2fdata.znds.com%2fattachment%2fforum%2f201606%2f09%2f175335zfpffn9n01g6e7z4.jpg&ehk=jv0b5QaSKQWKwZL0eTosZyNwCayFi%2fDhZO37B15WMoY%3d&risl=&pid=ImgRaw",
        "https://th.bing.com/th/id/R079c406a3776756370267d90ec863e21?rik=OXNlriAOVMpGbA&riu=http%3a%2f%2fwww.dnzhuti.com%2fuploads%2fallimg%2f170622%2f95-1F6221F344.jpg&ehk=0piGg7cwte86hjOqtYCPqdxZzR%2fK0eAv%2fzjoVgHjWCA%3d&risl=&pid=ImgRaw"
    ]

    tasks = [download_image(url=url) for url in urlist]
    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
