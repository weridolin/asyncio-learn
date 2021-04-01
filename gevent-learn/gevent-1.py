import gevent
from gevent import socket
import datetime
#  gevent.joinall: 等待所有元素执行完成 ,timeout:执行时间不超过2秒

urls = ['www.google.com', 'www.example.com', 'www.python.org']
jobs = [gevent.spawn(socket.gethostbyname, url) for url in urls]
_ = gevent.joinall(jobs,timeout=2) 
print([job.value for job in jobs]) 

# 非协程
for url in urls:
    r = socket.gethostbyname(url)
    print(r)


