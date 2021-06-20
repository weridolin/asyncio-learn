# -*- encoding: utf-8 -*-
# BEGIN YIELD_FROM_AVERAGER
from collections import namedtuple

Result = namedtuple('Result', 'count average')



####

# yield from x 表达式对x对象所做的第一件事是，
# 调用 iter(x),从中获取迭代器.因此,x可以是任何可迭代的对象。

# 1 让嵌套生成器不必通过循环迭代yield，而是直接yield from
def gen_one():
    subgen = range(10)
    yield from subgen

def gen_two():
    subgen = range(10)
    for item in subgen:
        yield item
# 2 在子生成器和原生成器的调用者之间打开双向通道，两者可以直接通信。

# yield可以直接作用于普通Python对象，而yield from却不行
# yield from <generator> OR  yield from <iterable>。
"""
    数据流通图                  
    
    调用方main                委派生成器grouper            子生成器averager
    
    send    --------------->                ------------>      
            <--------------                 <------------       yield     
    
    throw  ---------------->                 ------------>  
    close   --------------->                 ------------>
                                             <------------       stopIteration      
    
    委派生成器在 yield from 表达式处暂停时，调用方可以直 接把数据发给子生成器，
    子生成器再把产出的值发给调用方。子生成器返回之后，
    解释器会抛出 StopIteration 异常，并把返回值附 加到异常对象上，此时委派生成器会恢复
"""


# the subgenerator
def averager():  # <1>
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield  # <2>
        if term is None:  # <3> # 跳出循环，此时会抛出STOPITERATION
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)  # <4> 返回的 Result 会成为 grouper 函数中 yield from 表达式的值。


# the delegating generator
def grouper(results, key):  # <5>
    while True:  # <6>
        results[key] = yield from averager()  # <7>
    # grouper 发送的每个值都会经由 yield from 处理，通过管道传给 averager 实例。
    # grouper 会在 yield from 表达式处暂停，等待 averager 实例处理客户端发来的值。
    # averager 实例运行完毕后，返回的值绑定到 results[key] 上(此时不会抛出 stopIteration 异常)。
    # while 循环会不断创建 averager 实 例，处理更多的值

# the client code, a.k.a. the caller
def main(data):  # <8>
    results = {}
    for key, values in data.items():
        group = grouper(results, key)  # <9>group 是调用 grouper 函数得到的生成器对象，
                                            # 传给 grouper 函数 的第一个参数是 results，用于收集结果；
                                            # 第二个参数是某个 键。group 作为协程使用
        next(group)  # <10> 预激 group 协程。
        for value in values:
            group.send(value)  # <11>把各个 value 传给 grouper。传入的值最终到达 averager 函数中term = yield 那一行；grouper 永远不知道传入的值是什么

        group.send(None)  # important! <12> 把 None 传入 grouper，导致当前的 averager 实例终止，
                         # 也让 grouper(重新创建一个grouper) 继续运行，再创建一个 averager 实例，处理下一组值。

    # print(results)  # uncomment to debug
    report(results)


# output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
              result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


if __name__ == '__main__':
    main(data)

# END YIELD_FROM_AVERAGER
