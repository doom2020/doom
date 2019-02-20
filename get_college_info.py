"""此模块用来抓取中原工大学导师信息"""

import re
import requests
import time
import random



class CollegeInfo:
    def __init__(self):
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        self.basic_url = "https://see.zut.edu.cn/szdw/bsds.htm"
        self.part_url = "https://see.zut.edu.cn"
        self.person_url_list = []
    def get_source_list(self):
        # 创建请求并返回请求结果
        resp = requests.get(self.basic_url, headers=self.headers, proxies=None, timeout=None)
        # 对结果进行编码处理
        resp.encoding = "utf-8"
        # 获取页面的html
        source_list_page_html = resp.text
        # print(source_list_page_html)
        # 正则匹配页面内容提取所需文件url的列表
        pattern = re.compile('<a id=[\s\S]*?href="([\s\S]*?)"', re.S)
        source_result_list = re.findall(pattern, source_list_page_html)
        for source_result in source_result_list:
            person_url = self.part_url + source_result[2:]
            self.person_url_list.append(person_url)
        return self.person_url_list


    def get_source(self):
        person_url_list = self.get_source_list()
        for person_url in person_url_list:
            resp = requests.get(person_url, headers=self.headers, proxies=None, timeout=None)
            resp.encoding = "utf-8"
            source_page_html = resp.text
            # print(source_page_html)
            # 只匹配了姓名现在
            pattern = re.compile('<tr style="height:68px">.*?td width="113".*?<span.*?>(.*?)</span>', re.S)
            result_list = re.findall(pattern, source_page_html)
            print(result_list)

    def save_source2txt(self):
        pass
    def save_source2csv(self):
        pass
    def save_source2mysql(self):
        pass
    def save_source2mongo(self):
        pass
    def save_source2redis(self):
        pass

if __name__ == "__main__":
    college = CollegeInfo()
    college.get_source()