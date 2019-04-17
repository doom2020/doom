"""
Author:doom
datetime:2019.4.12
email:408575225@qq.com
github:doom2020
function: use selenium + phantomjs + chrome get shang hang hu li
comment:if you update my code,please update comment as too,thanks

"""
import requests
import re
import random
import time
import csv
from proxy_pool import *
from get_user_agent import get_user_agent
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from myLogger import LogHelper
import multiprocessing
import os
import threading


class ShangHaiHuLi:
    def __init__(self):
        self.basic_url = "http://shhl.ijournal.cn/ch/reader/key_query.aspx"
        self.detail_url = "http://shhl.ijournal.cn/ch/reader/"
        self.begin_page = 1
        self.end_page = 298
        self.headers = random.choice(get_user_agent())
        self.proxy_obj = ProxyPool()
        self.proxies = random.choice(self.proxy_obj.get_kuai())
        self.retry_count = 5
        self.timeout = 80
        self.encode_type = "utf-8"
        self.sleep_min = 1
        self.sleep_max = 2
        self.csv_save_basic_path = r"G:\shanghaihuli"
        self.file_name = os.path.join(self.csv_save_basic_path, 'shanghaihuli.csv')
        self.info_ls = []
        self.info_count = 0

    def get_page_html(self, i, retry_count):
        # 设置http代理
        socks5_proxy = '39.96.38.189:45990'
        proxy = "--proxy-server=socks5://" + socks5_proxy
        # headers = headers["User-Agent"]
        # 修改selenium请求设置
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('--headless')
        # chromeOptions.add_argument('--disable-gpu')
        # proxy = "--proxy-server=http://" + self.proxies["HTTP"]
        user_agent = "user-agent=" + self.headers["User-Agent"]
        chromeOptions.add_argument(proxy)
        chromeOptions.add_argument(user_agent)
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.set_page_load_timeout(random.randint(50, 80))
        try:
            driver.get(self.basic_url)
        except Exception as e:
            print("requests timeout:", e)
            driver.quit()
            return
        for n in range(1, 2):
            js = "var q=document.documentElement.scrollTop={}".format(n*20)
            driver.execute_script(js)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
        time.sleep(2)
        driver.find_element_by_id("to").send_keys(i)
        driver.find_element_by_id("go").click()
        time.sleep(random.randint(self.sleep_min, self.sleep_max))
        page_html = driver.page_source
        # print(page_html)
        time.sleep(2)
        driver.quit()
        self.get_page_href(page_html, i, retry_count)
        return self.info_ls

    def get_page_href(self, page_html, i, retry_count):
        html = etree.HTML(page_html)
        title_href_ls = html.xpath('//*[@id="DataGrid1"]/tbody//tr/td[1]/a/@href')
        title_ls = html.xpath('//*[@id="DataGrid1"]/tbody//tr/td[1]/a/text()[1]')
        count_href = len(title_href_ls)
        count_title = len(title_ls)
        if count_href != count_title:
            print("第{}页title_count not match href_count,原因:{}".format(i, "title_count > href_count" if count_href > count_title else "title_count < href_count"))
            return False
        for k in range(count_href):
            self.parse_info(title_href_ls[k], title_ls[k], retry_count)

    def parse_info(self, url, title, retry_count):
        url = self.detail_url + url
        # headers = random.choice(self.headers_ls)
        # proxies = random.choice(self.proxies_ls)
        try:
            resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
        except Exception as e:
            print(e)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            if retry_count == 0:
                print("详情页面请求失败")
                return False
            self.parse_info(url, title, retry_count-1)
        else:
            resp.encoding = self.encode_type
            page_html = resp.text
            self.get_info(page_html, title)

    def get_info(self, page_html, title):
        pattern = re.compile(r'<td nowrap>.*?<font.*?<u>(.*?)</u>.*?</font>.*?<font.*?<u>(.*?)</u>.*?</font>.*?<a.*?>(.*?)</a>', re.S)
        result_ls = re.findall(pattern, page_html)
        for x in result_ls:
            if "@" in x[-1]:
                title = title.strip()
                author = x[0].strip()
                position = x[1].strip()
                email = x[-1].strip()
                one_info = [title, author, position, email]
                self.info_ls.append(one_info)
                self.info_count += 1
                print("已抓取到{}条数据".format(self.info_count))


    def create_process_pool(self):
        # headers = random.choice(self.headers_ls)
        # proxies = random.choice(self.proxies_ls)
        p = multiprocessing.Pool()
        for i in range(self.begin_page, self.end_page):
            time.sleep(random.randint(1, 5))
            p.apply_async(func=self.get_page_html, args=(i, self.retry_count), callback=self.writer2csv)
        p.close()
        p.join()

    def writer2csv(self, result_ls):
        print("开始写入数据")
        first_line = ["title", "author", "position", "email"]
        with open(self.file_name, "a", newline="", encoding="utf-8", errors='ignore') as fw:
            writer = csv.writer(fw)
            writer.writerow(first_line)
            writer.writerows(result_ls)
        print("写入数据完成")


if __name__ == "__main__":
    shanghai = ShangHaiHuLi()
    shanghai.create_process_pool()
    print("此次爬虫任务已完成")