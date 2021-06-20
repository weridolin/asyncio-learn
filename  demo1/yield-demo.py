# -*- encoding: utf-8 -*-
# yield
def gen():
    yield 1
    yield 2
    yield 3
    yield 4

g = gen()
count= 1
while True:
    print(f"开始发送send:: 次数{count}")
    r = g.send(None)
    count+=1
    print(r)

## 什么时候抛出异常？ ---->当gen.send() gen执行后后续已经没有yield 关键字，即gen结束
