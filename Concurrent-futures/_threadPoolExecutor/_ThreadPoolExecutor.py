# -*- encoding: utf-8 -*-

# 了解之前可以先了解下 concurrent.futures
# concurrent.futures 提供异步执行调用的方法的抽象类。它不应该直接使用，而是通过它的具体子类使用。
# 线程池主要用于需要【创建大量线程并且线程的生命周期很短】的情况，线程池可以定义为一组预先实例化的空闲线程，它们随时准备接受工作。
# 当我们需要执行大量任务时，创建线程池比为每个任务实例化新线程要好。线程池可以管理大量线程的并发执行

# 线程池有两个特点
# 1 如果线程池中的线程完成了它的执行，那么该线程就可以被重用。
# 2 如果一个线程被终止，另一个线程将被创建来替换该线程。

# 参数
# initializer :Initializer是一个可选的可调用对象，它在每个工作线程开始时被调用;
# Initargs是传递给初始化器的参数元组。如果初始化器引发一个异常，所有当前挂起的作业将引发一个BrokenThreadPool，
# 以及任何向池提交更多作业的尝试都将引发异常

from concurrent.futures import ThreadPoolExecutor
from time import sleep


def task(message):
    sleep(2)
    return message


def singleTask():
    executor = ThreadPoolExecutor(5)
    future = executor.submit(task, ("Completed"))
    print(future.done())  # 任务还未完成,输出FALSE
    print(future.result())  # 如果此时任务还未完成，会一直阻塞等到任务完成
    # sleep(2)
    print(future.done())  # 任务完成，输出True
    print(future.result())  # 任务完成输出COMPLETED


def task2(message, index):
    sleep(2)
    if index == 3:
        raise AttributeError("raise exception test")
    return message


### 一次提交多个任务
import concurrent


def multiTasks(count=5):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(task2, "completed", i) for i in range(count)}
        print(futures)
        # 等待所有结果运行完成,return 一个generator
        # 这里generator的顺序跟submit的顺序相反的
        results = concurrent.futures.as_completed(futures)
        for r in results:
            try:
                print(r.result())
            except Exception as e:
                print(f">>>raise a exception:{e}")


## 提交的人任务多于 max_Works?
def task3(message, index):
    print(f">>>begin run task,index:{index}")
    sleep(2)
    if index % 3 == 0:
        raise AttributeError(f"raise exception test,index:{str(index)}")
    return f"{index}:{message}\n"


def submitsTasksMorethanMaxWorks():
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(task3, "completed", i): i for i in range(5)}
        print(futures)  # 查看future的状态，此时只有前5个是 running ,后面5个则为pending
        # 等待所有结果运行完成,return 一个generator
        # 这里generator的顺序并不是确定的
        results = concurrent.futures.as_completed(futures)
        print(results)
        while 1:
            try:
                # 每次generator 的输出并不是固定的顺序
                # 那么怎么能拿到顺序的输出呢，看下面!!!
                print(results.__next__())
            except StopIteration as e:
                print("no more result...")
                break


# 顺序拿到各个任务的输出 ---> map
def task4(message, index):
    sleep(2)
    # if index % 3 == 0:
    #     raise AttributeError(f">>>>raise a error :{index}")
    return message, index


def SortResults():
    indexes = (0, 1, 2, 3, 4)
    messages = ("complete", "complete", "complete", "complete", "complete")
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(task4, messages, indexes)
        print(results)
        # print(list(results))
        while 1:
            try:
                # 每次generator 的输出并不是固定的顺序
                # 输出的是固定顺序
                # 这里一旦raise A error 就会停止迭代了
                # 如果提交的TASKS数目比max_workers多，依然时按顺序来
                print(results.__next__())
            except StopIteration as e:
                print("no more result...")
                break
            except Exception as e:
                print(f"{e}")


# as_completed()函数接受一个Future对象的可迭代对象，一旦Future开始解析，就开始产生值。
# map方法与as_completed的主要区别在于map按照传递可迭代对象的顺序返回结果。map方法的第一个结果是第一个项目的结果。
# wait()方法，返回 tuplt(已经完成(包括异常),未完成)

##
def WaitResults():

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = {executor.submit(task4, "completed", i): i for i in range(5)}
        print(concurrent.futures.wait(
            results,
            return_when=concurrent.futures.ALL_COMPLETED))


if __name__ == '__main__':
    # singleTask()
    # print(f">>>>>>>>>>>>>>>>>>  multiTasks")
    # multiTasks()
    # print(f">>>>>>>>>>>>>>> submitsTasksMorethanMaxWorks")
    # submitsTasksMorethanMaxWorks()
    # print(f">>>>>>>>>>>>>>> SortResults")
    # SortResults()
    print(f">>>>>>>>>>>>>>> WaitResult")
    WaitResults()
