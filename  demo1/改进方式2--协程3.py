# -*- encoding: utf-8 -*-

import asyncio

# 1 没有了yield 或 yield from，而是async/await
#
# 2 没有了loop()，取而代之的是asyncio.get_event_loop()
#
# 3 无需自己在socket上做异步操作，不用显式地注册和注销事件，aiohttp库已经代劳
#
# 4 没有了显式的 Future 和 Task，asyncio已封装

import aiohttp

host = "http://example.com"
stopped = False
urls_to = ['/', '/1', '/2', '/3', '/4', '/5', '/6', '/7']

loop = asyncio.get_event_loop()


async def fetch(url):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            response = await response.read()
            return response


if __name__ == '__main__':
    import time

    start = time.time()
    tasks = [fetch(host + url) for url in urls_to]
    loop.run_until_complete(asyncio.gather(*tasks))
    print(time.time() - start)
