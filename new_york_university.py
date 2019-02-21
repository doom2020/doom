"""
author:doom
datetime:2019年2月21日
email:408575225@qq.com
github:doom2020
function:此模块用来抓取new york university导师信息
comment:if you want to update my code,please update the comment as too,thanks

"""

import re
import requests
import time
import random
import csv
from lxml import etree



class CollegeInfo:
    """初始化实例对象"""
    def __init__(self):
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        # 教授列表展示页url(这里需要更改)
        self.basic_url = "https://www.albany.edu/ceas/faculty-staff.php"
        self.part_url = "https://www.albany.edu"
        # 初始化教授url列表
        self.person_url_list = []
        # 学院(这里需要更改)
        self.college_name = "University at Albany - State University of New York"
        # 院系
        # self.college_department = "能源与环境学院"
        # 初始化教授信息列表(当然选择生成器是最好的)
        self.person_info_list = []
        # 设置csv文件基本存储路径
        self.basic_file_path = r'C:\Users\Administrator\Desktop'

    def get_source_list(self):
        """获取教授ulr列表"""
        # 创建请求并返回请求结果
        resp = requests.get(self.basic_url, headers=self.headers, proxies=None, timeout=60)
        # 对结果进行编码处理
        resp.encoding = "utf-8"
        # 获取页面的html
        source_list_page_html = resp.text
        # print(source_list_page_html)
        # 正则匹配页面内容提取所需文件url的列表,此处需分析打印出来的html文本，网页上匹配会出错，待分析原因
        pattern = re.compile('<div.*?<h3.*?<a href="(.*?)">', re.S)
        source_result_list = re.findall(pattern, source_list_page_html)
        # print(source_result_list)
        # print(len(source_result_list))
        for source_result in source_result_list:
            # 获取每个教授url
            person_url = self.part_url + source_result
            # print(person_url)
            self.person_url_list.append(person_url)
        # 返回值为每个教授url的列表
        # print(self.person_url_list)
        return self.person_url_list


    def get_source(self):
        """获取所有教授信息列表"""
        # 函数调用，获取每个教授的url列表
        person_url_list = self.get_source_list()
        for person_url in person_url_list:
            # 获取每个教授详情页信息
            resp = requests.get(person_url, headers=self.headers, proxies=None, timeout=80)
            resp.encoding = "utf-8"
            source_page_html = resp.text
            # (实践是检验真理的唯一标准，外国的网站写的代码就是规范呀，一样的结构很好抓(中国的网站结构很乱呀))用xpath提取需要内容吧，简单粗暴，xpath还能优化(3个有重复路径)
            html = etree.HTML(source_page_html)
            # 获取教授姓名(case:1)
            person_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[3]/div/strong[1]/span/text()')).strip('\n').strip("")
            if bool(person_name) == False:
                # case:2
                person_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[2]/div/strong[1]/span/text()')).strip('\n').strip("").strip('\r')
            # 获取院系
            college_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[3]/div/p/a[1]/strong/text()')).strip('\n').strip("").strip('\r')
            if bool(college_name) == False:
                # case:2
                college_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[2]/div/p/a/strong/text()')).strip('\n').strip("").strip('\r')
            # 获取部门
            department_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[3]/div/p/a[2]/text()')).strip('\n').strip("").strip('\r')
            if bool(department_name) == False:
                # case:2
                department_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[2]/div/p/text()')).strip('\n').strip("").strip('\r')
                if bool(department_name) == False:
                    # case:3
                    department_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[3]/div/p/text()')).strip('\n').strip("").strip('\r')
                    if bool(department_name) == False:
                        department_name = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[2]/div/p/a[2]/text()')).strip('\n').strip("").strip('\r')
            # 获取邮箱
            person_email = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[5]/a/text()')).strip('\n').strip("").strip('\r')
            if bool(person_email) == False:
                # case:2
                person_email = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[2]/div/div[5]/a/text()')).strip('\n').strip("").strip('\r')
                # case:3
                if bool(person_email) == False:
                    person_email = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[4]/a/text()')).strip('\n').strip("").strip('\r')
                    if bool(person_email) == False:
                        person_email = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[3]/div/div[3]/a/text()')).strip('\n').strip("").strip('\r')
                        if bool(person_email) == False:
                            person_email = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/div[2]/div/div[3]/a/text()')).strip('\n').strip("").strip('\r')
            # 研究领域
            research_interests = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[3]//text()')).strip('\n').strip("").strip('\r')
            '//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[2]'
            '//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[2]/text()[1]'
            '//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[2]/text()[2]'
            # 获取教授发表的最新论文
            person_article = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[5]/text()[2]')).strip('\n').strip("").strip('\r')
            if bool(person_article) == False:
                # case:2
                person_article = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[3]/text()[2]')).strip('\n').strip("").strip('\r')
                if bool(person_article) == False:
                    # case:3
                    person_article = "".join(html.xpath('//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[2]/text()')).strip('\n').strip("").strip('\r')
            '//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[3]/text()[2]'
            '//*[@id="content"]/div[1]/div/div/div[1]/div/div/div/p[2]/text()'
            # 用列表来存储每个教授的信息(也可以用字典或者元祖)
            person_one_info = [self.college_name, person_name, college_name, department_name, person_email, research_interests, person_article]
            self.person_info_list.append(person_one_info)
            # 返回值所有教授的信息列表
        return self.person_info_list

    def save_source2txt(self):
        """使用txt格式存储"""
        pass
    def save_source2csv(self):
        """使用csv格式存储"""
        # 设置文件名
        csv_file_name = r"\university_person_info.csv"
        # 文件绝对路径
        college_info_csv_file = self.basic_file_path + csv_file_name
        # 增加一行每列的标题
        title = ["校名", "姓名", "院系", "部门", "邮箱", "研究领域", "最新论文"]
        person_info_list = self.get_source()
        with open(college_info_csv_file, 'a', newline="", encoding="utf_8_sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(title)
            writer.writerows(person_info_list)
        print("全部存储完成")


    def save_source2mysql(self):
        """使用mysql数据库存储"""
        pass
    def save_source2mongo(self):
        """使用mongodb数据库存储"""
        pass
    def save_source2redis(self):
        """使用redis数据库存储"""
        pass

if __name__ == "__main__":
    college = CollegeInfo()
    college.save_source2csv()