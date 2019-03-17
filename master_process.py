import time
import queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support


class Master:
    def __init__(self):
        self.task_number = 10
        self.task_queue = queue.Queue(self.task_number)
        self.result_queue = queue.Queue(self.task_number)
        self.master_address = '127.0.0.1'
        self.master_port = 5000
        self.authkey = b'doom'
        self.timeout = 30
        self.result_list = []

    def save_result(self, result_one):
        self.result_list.append(result_one)
        print(self.result_list)
        return None

    def test_task(self, num):
        return num**2

    # def get_task(self):
    #     return self.task_queue
    #
    # def get_result(self):
    #     return self.result_queue

    def put_task_get_result(self):
        BaseManager.register('get_task_queue', callable=self.task_queue)
        BaseManager.register('get_result_queue', callable=self.result_queue)
        manager = BaseManager(address=(self.master_address, self.master_port), authkey=self.authkey)
        manager.start()
        try:
            task = manager.get_task_queue()
            result = manager.get_result_queue()
            # 添加任务
            for i in range(self.task_number):
                task_one = self.test_task(i)
                print("第一个任务是:", task_one)
                task.put(task_one)

            for i in range(self.task_number):
                result_one = result.get(self.timeout)
                print("第一个任务结果是:", result_one)
                self.save_result(result_one)
        except Exception as e:
            print("e")
            print("master exit abnormal")
            manager.shutdown()
        else:
            print("master normal exit")
            manager.shutdown()


if __name__ == "__main__":
    # freeze_support()
    task_result = Master()
    task_result.put_task_get_result()






