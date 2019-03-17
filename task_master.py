"""
author:doom
email:408575225
datetime:20190316
github:doom2020
function:此模块为实现分布式进程(分布任务，接收结果)

"""
import random
import time
import queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support


# def put_task_get_result():
# 发送任务的队列
task_queue = queue.Queue()
# 接收结果的队列
result_queue = queue.Queue()
class QueueManager(BaseManager):
    pass

def get_task():
    return task_queue

def get_result():
    return result_queue

def test():
    # 把两个Queue都注册到网络上，callable参数关联了Queue对象
    QueueManager.register('get_task_queue', callable=get_task)
    QueueManager.register('get_result_queue', callable=get_result)
    # 绑定端口5000,设置验证码'doom'
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'doom')
    # 启动Queue
    manager.start()
    # 获得通过网络访问的Queue对象
    try:
        task = manager.get_task_queue()
        result = manager.get_result_queue()
        # 放任务
        for i in range(10):
            n = random.randint(10, 1000)
            print('put task %d' % n)
            task.put(n)

        # 从result队列读取结果
        for i in range(10):
            r = result.get(timeout=30)
            print('result:{}'.format(r))
    except Exception as e:
        print(e)
        print('master abnormal exit')
        manager.shutdown()
    else:
        # 关闭任务
        manager.shutdown()
        print('master exit')

if __name__ == "__main__":
    test()
#     put_task_get_result()