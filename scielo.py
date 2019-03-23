"""
Author:doom
datetime:2019.3.22
email:408575225@qq.com
github:doom2020
function: use selenium + phantomjs + chrome model journal
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


class ScientificElectronicLibraryOnline:
    def __init__(self):
        self.basic_url = "https://www.scielo.org/en/journals/list-by-subject-area/5/agricultural-sciences"
        self.classify = "Agricultural_Sciences"
        self.headers = random.choice(get_user_agent())
        self.proxy_obj = ProxyPool()
        self.proxies = random.choice(self.proxy_obj.get_xici())
        self.url_list = []
        self.retry_count = 5
        self.timeout = 80
        self.encode_type = "utf-8"
        self.sleep_min = 1
        self.sleep_max = 3
        self.csv_save_basic_path = r"G:\scielo_20190322"
        self.file_name = os.path.join(self.csv_save_basic_path, 'scielo.csv')
        self.line_count = 0
        # self.logger = LogHelper()

    def test_first_page(self):
        # VPN socks5代理ip和端口
        socks5_proxy = '39.96.38.189:45990'
        # 修改selenium请求设置
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('--headless')
        # chromeOptions.add_argument('--disable-gpu')
        proxy = "--proxy-server=socks5://" + socks5_proxy
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
            # self.logger.writeLog("一级页面请求失败", level="error")
            return
        js1 = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js1)
        time.sleep(2)
        js2 = "var q=document.documentElement.scrollTop=12000"
        driver.execute_script(js2)
        time.sleep(2)
        js3 = "var q=document.documentElement.scrollTop=16000"
        driver.execute_script(js3)
        time.sleep(6)
        page_html = driver.page_source
        time.sleep(2)
        driver.quit()
        self.parse_first_page(page_html)

    def parse_first_page(self, page_html):
        pattern = re.compile(r'<tr.*?<a href="(.*?)">.*?<strong class="journalTitle">(.*?)</strong>.*?</tr>', re.S)
        result_list = re.findall(pattern, page_html)
        if not result_list:
            print("第一级页面解析失败")
            # self.logger.writeLog("一级页面解析失败", level="error")
            return False
        for i in result_list[1:]:
            try:
                title = i[-1].split("\n")[-1].strip()
                # 这里的href要做处理
                href = i[0].replace("amp;", "")
            except IndexError:
                continue
            tuple_one = (href, title)
            self.url_list.append(tuple_one)
        print("url总数:", len(self.url_list))
        time.sleep(2)
        # 创建多进程
        p_lock = multiprocessing.Lock()
        for tuple_one in self.url_list:
            p = multiprocessing.Process(target=self.test_second_page, args=(tuple_one, self.retry_count, p_lock))
            p.start()
            p.join()
        print("所有进程执行完毕")

    def test_second_page(self, tuple_one, retry_count, p_lock):
        print("当前进程pid:{},ppid:{}".format(os.getpid(), os.getppid()))
        url = tuple_one[0]
        journal_name = tuple_one[1]
        try:
            resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
        except Exception as e:
            print(e)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            if retry_count == 0:
                # self.logger.writeLog("二级页面请求失败url:{}".format(url), level="error")
                return False
            self.test_second_page(tuple_one, retry_count-1, p_lock)
        else:
            resp.encoding = self.encode_type
            page_html = resp.text
            self.parse_second_page(page_html, journal_name, p_lock)

    def parse_second_page(self, page_html, journal_name, p_lock):
        html = etree.HTML(page_html)
        result_list = html.xpath("/html/body/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/a[1]/@href")
        try:
            url = result_list[0]
        except IndexError:
            # self.logger.writeLog("二级页面解析失败", level="error")
            return False
        self.test_third_page(url, journal_name, p_lock, self.retry_count)

    def test_third_page(self, url, journal_name, p_lock, retry_count):
        try:
            resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
        except Exception as e:
            print(e)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            if retry_count == 0:
                # self.logger.writeLog("三级页面请求失败url:{}".format(url), level="error")
                return False
            self.test_third_page(url, journal_name, p_lock, retry_count-1)
        else:
            resp.encoding = self.encode_type
            page_html = resp.text
            self.parse_third_page(page_html, journal_name, p_lock)

    def parse_third_page(self, page_html, journal_name, p_lock):
        html = etree.HTML(page_html)
        result_list = html.xpath("/html/body/div[1]/table[2]/tbody/tr/td[2]/table/tbody//tr//td//b//font/a/@href")
        if not result_list:
            # self.logger.writeLog("三级页面解析失败", level="error")
            return False
        t_lock = threading.Lock()
        for url in result_list:
            t = threading.Thread(target=self.test_fourth_page, args=(url, journal_name, p_lock, t_lock, self.retry_count))
            t.start()
            t.join()
        print("当前进程的所有线程执行完毕")

    def test_fourth_page(self, url, journal_name, p_lock, t_lock, retry_count):
        print("当前线程的pid:{},ppid:{}".format(os.getpid(), os.getppid()))
        try:
            resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
        except Exception as e:
            print(e)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            if retry_count == 0:
                # self.logger.writeLog("四级页面请求失败url:{}".format(url), level="error")
                return False
            self.test_fourth_page(url, journal_name, p_lock, t_lock, retry_count-1)
        else:
            resp.encoding = self.encode_type
            page_html = resp.text
            self.parse_fourth_page(page_html, journal_name, p_lock, t_lock)

    def parse_fourth_page(self, page_html, journal_name, p_lock, t_lock):
        html = etree.HTML(page_html)
        result_list = html.xpath("/html/body/div[1]/table/tbody/tr/td[2]/table/tbody//tr/td[2]/div/a[3]/@href")
        if not result_list:
            # self.logger.writeLog("四级页面解析失败", level="error")
            return False
        self.test_detail_page(result_list, journal_name, p_lock, t_lock, self.retry_count)

    def test_detail_page(self, result_list, journal_name, p_lock, t_lock, retry_count):
        for url in result_list:
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            try:
                resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
            except Exception as e:
                print(e)
                time.sleep(random.randint(self.sleep_min, self.sleep_max))
                if retry_count == 0:
                    # self.logger.writeLog("详情页面请求失败url:{}".format(url), level="error")
                    print("详情页面请求失败url:{}".format(url))
                    continue
                self.test_detail_page(result_list, journal_name, p_lock, t_lock, retry_count - 1)
            else:
                resp.encoding = self.encode_type
                page_html = resp.text
                self.parse_detail_page(url, page_html, journal_name, p_lock, t_lock)

    def parse_detail_page(self, url, page_html, journal_name, p_lock, t_lock):
        # case1(适用于2017-2019)
        html = etree.HTML(page_html)
        email_ls = re.findall(r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", page_html)
        if not email_ls:
            # self.logger.writeLog("详情页面获取邮箱失败url:{}".format(url), level="error")
            print("详情页面获取邮箱失败url:{}".format(url))
            return False
        for i in email_ls:
            if i == "actaagron@uem.br" or "gov." in i:
                email_ls.remove(i)
        try:
            email = email_ls[0]
        except IndexError:
            print("邮箱后缀为gov,无效邮箱")
            return False
        result_list1 = html.xpath('//*[@id="article-front"]/div[3]//p//text()')
        result1_str = "".join(result_list1)
        result_list2 = html.xpath('//*[@id="article-front"]/div[2]//p//text()')
        result2_str = "".join(result_list2)
        result_list3 = html.xpath('//*[@id="article-front"]/div[3]//text()')
        result3_str = "".join(result_list3)
        result_list4 = html.xpath("/html/body/div[1]/div[2]/div[2]/p[8]/font/b//text()")
        result4_str = "".join(result_list4)
        # case:1(after 2016 year)
        if "*" in result1_str:
            result_ls = result1_str.split("\n")
            for i in result_ls:
                if "*" in i:
                    index_a = result_ls.index(i)
                    try:
                        author = result_ls[index_a-1].replace("t", "").replace("1", "").replace("2", "").replace("3", "").strip()
                    except IndexError:
                        author = result_ls[index_a].replace("t", "").replace("1", "").replace("2", "").replace("3", "").replace("*", "").replace(",", "").strip()
                        info = [self.classify, journal_name, author, email]
                        self.save_to_csv(info, p_lock, t_lock)
                    if not author:
                        author = result_ls[index_a].replace("t", "").replace("1", "").replace("2", "").replace("3", "").replace("*", "").replace(",", "").strip()
                    info = [self.classify, journal_name, author, email]
                    self.save_to_csv(info, p_lock, t_lock)
                else:
                    pass
        # case:2(after 2016 year)
        elif "*" in result2_str:
            result_ls = result2_str.split("\n")
            for i in result_ls:
                if "*" in i:
                    index_a = result_ls.index(i)
                    try:
                        author = result_ls[index_a - 1].replace("t", "").replace("1", "").replace("2", "").replace("3", "").strip()
                    except IndexError:
                        author = result_ls[index_a].replace("t", "").replace("1", "").replace("2", "").replace("3", "").replace("*", "").replace(",", "").strip()
                        info = [self.classify, journal_name, author, email]
                        self.save_to_csv(info, p_lock, t_lock)
                    if not author:
                        author = result_ls[index_a].replace("t", "").replace("1", "").replace("2", "").replace("3", "").replace("*", "").replace(",", "").strip()
                    info = [self.classify, journal_name, author, email]
                    self.save_to_csv(info, p_lock, t_lock)
                else:
                    pass
        # case:3(after 2016 year)
        elif "*" in result3_str:
            result_ls = result3_str.split("\n")
            for i in result_ls:
                if "*" in i:
                    index_a = result_ls.index(i)
                    try:
                        author = result_ls[index_a - 1].replace("t", "").replace("1", "").replace("2", "").replace("3", "").replace(",", "").strip()
                    except IndexError:
                        author = result_ls[index_a].replace("t", "").replace("1", "").replace("2", "").replace("3", "").replace("*", "").replace(",", "").strip()
                        info = [self.classify, journal_name, author, email]
                        self.save_to_csv(info, p_lock, t_lock)
                    if not author:
                        author = result_ls[index_a].replace("t", "").replace("1", "").replace("2", "").replace("3", "").replace("*", "").replace(",", "").strip()
                    info = [self.classify, journal_name, author, email]
                    self.save_to_csv(info, p_lock, t_lock)
                else:
                    pass
        # case:4(before 2016 year)
        elif "*" in result4_str:
            result_ls = result4_str.split(";")
            for i in result_ls:
                if "*" in i:
                    index_a = result_ls.index(i)
                    author = result_ls[index_a].replace("*", "").replace("I", "").replace("II", "").replace("III", "").replace(",", "").strip()
                    info = [self.classify, journal_name, author, email]
                    self.save_to_csv(info, p_lock, t_lock)
                else:
                    pass
        else:
            # self.logger.writeLog("详情页面获取信息失败url:{}".format(url), level="error")
            print("详情页获取信息失败url:{}".format(url))

    def save_to_csv(self, info, p_lock, t_lock):
        print("上进程锁")
        p_lock.acquire()
        print("上线程锁")
        t_lock.acquire()
        try:
            with open(self.file_name, "a", newline="", encoding="utf-8", errors='ignore') as fw:
                writer = csv.writer(fw)
                writer.writerow(info)
        except Exception as e:
            print(e)
            print("此条数据插入失败")
            print("释放线程锁")
            t_lock.release()
            print("释放进程锁")
            p_lock.release()
        self.line_count += 1
        # self.logger.writeLog("当前写入的数据量{}个".format(self.line_count), level="info")
        print("当前已写入了{}条有效数据".format(self.line_count))
        print("文件写入成功啦")
        print("释放线程锁")
        t_lock.release()
        print("释放进程锁")
        p_lock.release()
        print("save to csv 函数执行完成")


if __name__ == "__main__":
    journal = ScientificElectronicLibraryOnline()
    journal.test_first_page()