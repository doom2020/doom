"""
author:doom
email:408575225
datetime:20190316
github:doom2020
function:此模块为实现分布式进程(处理任务)

"""
import time
import sys
import queue
from multiprocessing.managers import BaseManager

def finish_work():
    # 创建QueueManager
    class QueueManager(BaseManager):
        pass
    # 由于这个QueueManager只是从网络上获取Queue,所以注册时只提供名字
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    # 连接到服务器(分布任务的机器)
    server_address = '127.0.0.1'
    print('connect to server %s success' % server_address)
    # 端口和验证码保持与task_master.py设置完全一样
    manager = QueueManager(address=(server_address, 5000), authkey=b'doom')
    # 从网络连接
    manager.connect()
    # 获取Queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    # 从task队列取任务，并把结果写入到result队列
    for i in range(10):
        try:
            n = task.get(timeout=1)
            print('run task %d * %d' % (n, n))
            r = '%d * %d = %d' % (n, n, n*n)
            time.sleep(1)
            result.put(r)
        except queue.Queue.Empty:
            print('task queue is empty')

    print('work exit')

if __name__ == "__main__":
    finish_work()





