# -*- encoding: utf-8 -*-

# multiprocess:     多进程，充分利用了多个CPU ，[并行]运行,
# Multithreading:   单个CPU通过[并发]执行多个线程.多线程的主要思想是通过将一个进程划分为多个线程来实现并行性

# fork,只适用于unix/linux
# 它用于创建称为子进程的新进程。此子进程与称为父进程的进程[并发]运行。
# 这些子进程也与它们的父进程相同，并继承父进程可用的所有资源
import os

def child():
    n = os.fork()
    if n > 0:
        print("PID of Parent process is : ", os.getpid())
    else:
        print("PID of Child process is : ", os.getpid())


# Spawn,启动时间较长，启动一个全新的进程

# 1 Importing multiprocessing module.
# 2 Creating the object process.
# 3 Starting the process activity by calling start() method.
# 4 Waiting until the process has finished its work and exit by calling join() method.



import multiprocessing,time

def spawn_process(i):
    print('This is process: %s' % i)
    time.sleep(2)
    return

def SpwanProcess():
    Process_jobs = []
    for i in range(3):
        p = multiprocessing.Process(target = spawn_process, args = (i,))
        Process_jobs.append(p)
        p.start()
        print(p.pid)
        # p.join()

# Daemon process
# 守护进程或在后台运行的进程遵循与守护线程类似的概念。
# 要在后台执行该进程，我们需要将守护进程标志设置为true。
# 只要主进程正在执行，守护进程将继续运行，它将在主进程执行完毕或主程序被杀死后终止

def nondaemonProcess():
   print("starting my Process")
   time.sleep(8)
   print("ending my Process")
def daemonProcess():
   while True:
       print("Hello")
       time.sleep(2)
def daemonProcessStart():
   nondaemonProcess1 = multiprocessing.Process(target = nondaemonProcess)
   daemonProcess1 = multiprocessing.Process(target = daemonProcess)
   daemonProcess1.daemon = True
   nondaemonProcess1.daemon = False
   daemonProcess1.start()
   nondaemonProcess1.start()

# if __name__ == '__main__':
    # 注意这里守护进程的输出不会打印到控制台
   # daemonProcessStart()

# 进程终止: terminate
# 使用terminate()方法立即终止或终止一个进程。我们将使用此方法在完成执行之前立即终止子进程
import multiprocessing
import time
def Child_process():
   print ('Starting function')
   time.sleep(5)
   print ('Finished function')
P = multiprocessing.Process(target = Child_process)
P.start()
print("My Process has terminated, terminating main thread")
print("Terminating Child Process")
P.terminate()
print("Child Process successfully terminated")
