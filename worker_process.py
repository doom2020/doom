import time
import sys
import queue
import random
from multiprocessing.managers import BaseManager

class Worker:
    def __init__(self):
        self.master_address = '127.0.0.1'
        self.master_port = 6666
        self.master_authkey = b'doom'
        self.timeout = 3
        self.task_number = 0
        self.sleep_time = random.randint(0, 3)

    def get_task_put_result(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        manager = BaseManager(address=(self.master_address, self.master_port), authkey=self.master_authkey)
        try:
            manager.connect()
        except Exception as e:
            print(e)
            print("连接master host fail")
            sys.exit()
        else:
            task = manager.get_task_queue()
            result = manager.get_result_queue()
            while not task.empyt():
                self.task_number += 1
                task_one = task.get(timeout=self.timeout)
                print("master 分配的第{}个任务:{}".format(self.task_number, task_one))
                time.sleep(self.sleep_time)
                result_one = '我是任务{}的结果'.format(self.task_number)
                result.put(result_one)

if __name__ == "__main__":
    worker = Worker()
    worker.get_task_put_result()

