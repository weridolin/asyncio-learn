# -*- encoding: utf-8 -*-
# -*- encoding: utf-8 -*-
import socket
import selectors

# 让epoll代替应用程序监听socket状态时，得告诉epoll：
# “如果socket状态变为可以往里写数据（连接建立成功了），

# 请调用HTTP请求发送函数。如果socket 变为可以读数据了（客户端已收到响应），
# 请调用响应处理函数。

selector = selectors.DefaultSelector()
stopped = False
urls_to = ['/','/1','/2','/3','/4','/5','/6','/7']

class Crawler:
    def __init__(self,url):
        self.url= url
        self.sock=None
        self.response=b""

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False) # false时 当调用connect和recv不会阻塞
        try:
            self.sock.connect(("example.com",80))
        except BlockingIOError:
            pass
        # 当socket 为可写状态，即为connect时，触发connected事件
        selector.register(self.sock.fileno(),selectors.EVENT_WRITE,self.connected)

    def connected(self,key,mask):
        selector.unregister(key.fd)# 取消 self.fetch 注册的回调事件

        get = 'GET{0}HTTP/1.0 \r\n host:example.com'.format(self.url)
        self.sock.send(get.encode("ascii"))
        selector.register(key.fd, selectors.EVENT_READ, self.read_response)

    def read_response(self,key,mask):
        global stopped
        chunk = self.sock.recv(4096)
        if chunk:
            self.response+=chunk
        else:
            selector.unregister(key.fd)
            urls_to.remove(self.url)
            if not urls_to:
                stopped=False

#  Event loop 从selector里获取当前正发生的事件，并且得到对应的回调函数去执行
def loop():
    while not stopped:
        # 阻塞轮询直到有一个事件发生
        events = selector.select()
        for event_key,event_mask in events:
            callback = event_key.data
            callback(event_key,event_mask)

if __name__ == '__main__':
    import time
    start = time.time()
    for url in urls_to:
        crawler  = Crawler(url)
        crawler.fetch()
    loop()
    print(time.time()-start)
# 1 创建Crawler 实例；
#
# 2 调用fetch方法，会创建socket连接和在selector上注册可写事件；
#
# 3 fetch内并无阻塞操作，该方法立即返回；
#
# 4 重复上述3个步骤，将10个不同的下载任务都加入事件循环；
#
# 5 启动事件循环，进入第1轮循环，阻塞在事件监听上；
#
# 6 当某个下载任务EVENT_WRITE被触发，回调其connected方法，第一轮事件循环结束；
#
# 7 进入第2轮事件循环，当某个下载任务有事件触发，执行其回调函数；此时已经不能推测是哪个事件发生，
# 因为有可能是上次connected里的EVENT_READ先被触发，也可能是其他某个任务的EVENT_WRITE被触发；
# （此时，原来在一个下载任务上会阻塞的那段时间被利用起来执行另一个下载任务了）

# 8 循环往复，直至所有下载任务被处理完成

# 9 退出事件循环，结束整个下载程序



###
