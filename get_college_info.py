"""
author:doom
datetime:2019年2月21日
email:408575225@qq.com
github:doom2020
function:此模块用来抓取中原工大学导师信息
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
        self.basic_url = "https://see.zut.edu.cn/szdw/bsds.htm"
        self.part_url = "https://see.zut.edu.cn"
        # 初始化教授url列表
        self.person_url_list = []
        # 学院
        self.college_name = "中原工学院"
        # 院系
        # self.college_department = "能源与环境学院"
        # 初始化教授信息列表(当然选择生成器是最好的)
        self.person_info_list = []
        # 设置csv文件基本存储路径
        self.basic_file_path = r'C:\Users\Administrator\Desktop'

    def get_source_list(self):
        """获取教授ulr列表"""
        # 创建请求并返回请求结果
        resp = requests.get(self.basic_url, headers=self.headers, proxies=None, timeout=None)
        # 对结果进行编码处理
        resp.encoding = "utf-8"
        # 获取页面的html
        source_list_page_html = resp.text
        # print(source_list_page_html)
        # 正则匹配页面内容提取所需文件url的列表,此处需分析打印出来的html文本，网页上匹配会出错，待分析原因
        pattern = re.compile('<a id=[\s\S]*?href="([\s\S]*?)"', re.S)
        source_result_list = re.findall(pattern, source_list_page_html)
        for source_result in source_result_list:
            # 获取每个教授url，切片处理将"//"去除
            person_url = self.part_url + source_result[2:]
            self.person_url_list.append(person_url)
        # 返回值为每个教授url的列表
        return self.person_url_list


    def get_source(self):
        """获取所有教授信息列表"""
        # 函数调用，获取每个教授的url列表
        person_url_list = self.get_source_list()
        for person_url in person_url_list:
            # 获取每个教授详情页信息
            resp = requests.get(person_url, headers=self.headers, proxies=None, timeout=None)
            resp.encoding = "utf-8"
            source_page_html = resp.text
            # print(source_page_html)
            # 获取院系
            pattern = re.compile('<table.*?<img src.*?title="(.*?)">', re.S)
            department_name = re.findall(pattern, source_page_html)[0]
            # (你看看原页面代码就知道为什么不用正则了，这tm是多少年前写的东西，看得眼都花了)用xpath提取需要内容吧，简单粗暴，xpath还能优化(3个有重复路径)
            html = etree.HTML(source_page_html)
            print(department_name)
            # 获取教授姓名(切片去除引号和中括号两边的)
            person_name = str(html.xpath('//*[@id="vsb_content"]/div/div/table/tbody/tr[2]/td[2]/p/span/text()'))[2:-2]
            # 获取教授最新的论文(这里是一个列表哦，需要拼接一下，看下面的for循环)
            person_article_split_list = html.xpath('//*[@id="vsb_content"]/div/div/table/tbody/tr[12]/td/p[last()-1]//span/text()')
            # 获取教授的email，使用join拼接字符串
            # 邮箱这里又有坑格式不一样(5种情况)case:1
            person_email = "".join(html.xpath('//*[@id="vsb_content"]/div/div/table/tbody/tr[18]/td//p[last()-2]//span[2]/span/text()'))
            is_vaild_email_length_lt = 14
            if bool(person_email) == False:
                # case:2
                person_email = "".join(html.xpath('//*[@id="vsb_content"]/div/div/table/tbody/tr[18]/td/p[last()-2]/span[2]/text()'))
                if bool(person_email) == False:
                    # case:3
                    person_email = "".join(html.xpath('//*[@id="vsb_content"]/div/div/table/tbody/tr[18]/td/p[last()-2]/span[2]/span/a/text()'))
                # 判断字符串长度小于14要用新规则抓取
                elif len(str(person_email)) < is_vaild_email_length_lt:
                    # case:4
                    person_email = "".join(html.xpath('//*[@id="vsb_content"]/div/div/table/tbody/tr[18]/td/p[last()-2]/span[position()<3]//text()')[1:])
            elif len(str(person_email)) < is_vaild_email_length_lt:
                # case:5
                person_email = "".join(html.xpath('//*[@id="vsb_content"]/div/div/table/tbody/tr[18]/td/p[last()-2]/span[position()<3]/span/text()'))
            # 初始化文章
            person_article = ""
            # 去除前面序号
            for i in person_article_split_list[1:]:
                person_article += i
            # 用列表来存储每个教授的信息(也可以用字典或者元祖)
            person_one_info = [self.college_name, department_name, person_name, person_article, person_email]
            self.person_info_list.append(person_one_info)
            # 返回值所有教授的信息列表
        return self.person_info_list

    def save_source2txt(self):
        """使用txt格式存储"""
        pass
    def save_source2csv(self):
        """使用csv格式存储"""
        # 设置文件名
        csv_file_name = r"\college_person_info.csv"
        # 文件绝对路径
        college_info_csv_file = self.basic_file_path + csv_file_name
        # 增加一行每列的标题
        title = ["院校", "院系", "姓名", "最新论文", "邮箱"]
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