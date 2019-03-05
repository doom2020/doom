"""

Author:doom
datetime:2019.3.5
email:408575225@qq.com
github:doom2020
function: get qin hua college info
comment: if you update my code,please update the comment,thanks

"""
import requests
import re
from lxml import etree
from get_user_agent import get_user_agent
from proxy_pool import *
from myLogger import LogHelper
import os
import time
import random
import multiprocessing
import csv



class QinHuaCollege:
    # 外部类属性
    # 1.创建User-Agent池
    user_agent_list = get_user_agent()
    # 1.创建User-Agent池
    proxies = None
    # 3.请求超时时间设定
    timeout = 20

    def __init__(self):
        # 外部类对象的属性
        # # 1.创建User-Agent池
        # self.user_agent_list = get_user_agent()
        # # 1.创建User-Agent池
        # self.proxies = None
        # # 3.请求超时时间设定
        # self.timeout = 20
        pass

    @classmethod
    def deal_with_request_abnormal(cls):  # 外部类方法
        """异常处理方法"""
        pass

    def example(self):  # 外部类对象方法
        pass

    # 内部类(清华大学医学院)
    class MedicineDepartment:
        def __init__(self):
            # 1.基础医学系
            self.department_first_url = "http://www.med.tsinghua.edu.cn/Person?method=101"
            # 2.生物医学工程
            self.department__second_url = "http://www.med.tsinghua.edu.cn/Person?method=101&param=124"
            # 3.公共健康研究中心
            self.department__third_url = "http://www.med.tsinghua.edu.cn/Person?method=101&param=125"
            # 4.存储基本路径
            self.save_basic_path = r"C:\Users\Administrator\Desktop"
            self.file_name = "file_name"
            self.file = os.path.join(self.save_basic_path, self.file_name)
            # 5.每位老师初始url
            self.basic_url = "http://www.med.tsinghua.edu.cn/"

        def get_all_teachers_href(self):
            # 调用外部类属性
            headers = random.choice(QinHuaCollege.user_agent_list)
            try:
                resp = requests.get(self.department_first_url, headers=headers, proxies=QinHuaCollege.proxies, timeout=QinHuaCollege.timeout)
            except TimeoutError:
                print("time over")
                return
            time.sleep(5)
            resp.encoding = "utf-8"
            page_html = resp.text
            pattern = re.compile('<li>.*?<a href="(.*?)">(.*?)</a>.*?</li>', re.S)
            result_list = re.findall(pattern, page_html)[:-4]
            print(result_list)
            for result in result_list:
                url = self.basic_url + result[0]
                name = result[1].strip()
                url_name = (url, name)
                p_lock = multiprocessing.Lock()
                p = multiprocessing.Process(target=self.get_teachers_info, args=(url_name, p_lock))
                p.start()
                p.join()
            print("all process is over")

        def get_teachers_info(self, url_name, p_lock):
            url = url_name[0]
            name = url_name[1]
            # 调用外部类属性
            headers = random.choice(QinHuaCollege.user_agent_list)
            try:
                time.sleep(random.randint(1, 2))
                resp = requests.get(url, headers=headers, proxies=QinHuaCollege.proxies,
                                    timeout=QinHuaCollege.timeout)
            except TimeoutError:
                print("time over")
                return
            resp.encoding = "utf-8"
            page_html = resp.text
            # 匹配系别
            pattern = re.compile('<h2 class="current_position_title">(.*?)</h2>', re.S)
            department_list = re.findall(pattern, page_html)
            department = department_list[0]
            html = etree.HTML(page_html)
            # 研究领域
            '/html/body/div[3]/div/div[2]'
            '/html/body/div[3]/div/div[2]'
            '/html/body/div[3]/div/div[2]//p/span/text()'
            references_list = html.xpath('/html/body/div[3]/div/div[2]//p/span/text()')
            references = "".join(references_list)
            # 邮箱
            '/html/body/div[3]/div/div[6]/p[1]'
            email_list = html.xpath('/html/body/div[3]/div/div[6]/p[1]/text()')
            email = email_list[0]
            info = [department, name, references, email]
            self.save_info2csv(info, p_lock)

        def save_info2csv(self, info, p_lock):
            p_lock.acquire()
            with open(self.file, 'a', newline="", encoding="gbk") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(info)
            p_lock.release()

    # 内部类(清华大学生命科学学院)
    class LifeSciencesDepartment:
        def __int__(self):
            pass

if __name__ == "__main__":
    # 创建外部类的实例
    college = QinHuaCollege()
    # 创建内部类的实例
    # department = college.MedicineDepartment()
    # # 调用内部类的方法
    # department.get_all_teachers_href()
