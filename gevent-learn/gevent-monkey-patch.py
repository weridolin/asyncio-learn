import gevent
from gevent import monkey

monkey.patch_all()
# monkey.patch_all() : 
# 1 gevent 无法捕获普通的耗时操作, 那么遇见耗时操作只会傻傻等待，
# 2 但是我们需要切换另外的协程去执行，同时我们又不想改变原来的代码；
# 3 那么我们就需要以打补丁的形式去处理这样的问题，this is monkey.patch_all()


# issue1: RecursionError: maximum recursion depth exceeded while calling a Python object（超过最大递归深度） 
# 注意1： monkey.patch_all()最好在程序开始就调用， 


import time

def task1():
    for i in range(10):
        time.sleep(0.1)
        print("1:%s",i)

def task2():
    for i in range(10):
        time.sleep(0.1)
        print("2:%s",i)


# jobs = [gevent.spawn(task1),gevent.spawn(task2)]
# gevent.joinall(jobs)

# 不加     monkey.patch_all()
# 1:%s 0
# 1:%s 1
# 1:%s 2
# 1:%s 3
# 1:%s 4
# 1:%s 5
# 1:%s 6
# 1:%s 7
# 1:%s 8
# 1:%s 9
# 2:%s 0
# 2:%s 1
# 2:%s 2
# 2:%s 3
# 2:%s 4
# 2:%s 5
# 2:%s 6
# 2:%s 7
# 2:%s 8
# 2:%s 9


# 加了 monkey.patch_all()
# monkey.patch_all()

# jobs = [gevent.spawn(task1),gevent.spawn(task2)]
# gevent.joinall(jobs)

# output:
# 1:%s 0
# 2:%s 0
# 1:%s 1
# 2:%s 1
# 1:%s 2
# 2:%s 2
# 1:%s 3
# 2:%s 3
# 1:%s 4
# 2:%s 4
# 1:%s 5
# 2:%s 5
# 1:%s 6
# 2:%s 6
# 1:%s 7
# 2:%s 7
# 1:%s 8
# 2:%s 8
# 1:%s 9
# 2:%s 9



## Demo 下载图片测试
import requests

urlist=[
    "https://th.bing.com/th/id/Rf27c1a2fe19310a12b595063e8a57e17?rik=gM7Zu1QoOaSTmQ&riu=http%3a%2f%2fwww.dnzhuti.com%2fuploads%2fallimg%2f161230%2f95-161230160H0.jpg&ehk=R9HqrAVAoWSdhWbxLlCAldyrM1EY4Ho5%2faPMEUP5aYE%3d&risl=&pid=ImgRaw",
    "https://th.bing.com/th/id/Rc2c19809bf2fe6394a76b2e7d9ec156d?rik=2kVroExkhAd%2bpw&riu=http%3a%2f%2fdata.znds.com%2fattachment%2fforum%2f201606%2f09%2f175335zfpffn9n01g6e7z4.jpg&ehk=jv0b5QaSKQWKwZL0eTosZyNwCayFi%2fDhZO37B15WMoY%3d&risl=&pid=ImgRaw",
    "https://th.bing.com/th/id/R079c406a3776756370267d90ec863e21?rik=OXNlriAOVMpGbA&riu=http%3a%2f%2fwww.dnzhuti.com%2fuploads%2fallimg%2f170622%2f95-1F6221F344.jpg&ehk=0piGg7cwte86hjOqtYCPqdxZzR%2fK0eAv%2fzjoVgHjWCA%3d&risl=&pid=ImgRaw"
]

def download_pic(url,index):
    print(f"download image :{str(index)} ")
    res = requests.get(url)
    filename = url[40:50]+'.jpg'
    with open(filename,mode="wb") as file_object:
        file_object.write(res.content) 
    print(f"download image :{str(index)} finish")

# tasks = [gevent.spawn(download_pic,url,index) for index,url in enumerate(urlist)]
# gevent.joinall(tasks)

# no monkey.patch()
# download image :0
# download image :0 finish
# download image :1
# download image :1 finish
# download image :2
# download image :2 finish



tasks = [gevent.spawn(download_pic,url,index) for index,url in enumerate(urlist)]
gevent.joinall(tasks)
# with monkey.patch()
# download image :0
# download image :1
# download image :2
# download image :0 finish
# download image :2 finish
# download image :1 finish