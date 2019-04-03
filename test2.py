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
        self.basic_url = "https://www.scielo.org/en/journals/list-by-subject-area/7/biological-sciences"
        self.classify = "Biological_Sciences"
        self.headers = random.choice(get_user_agent())
        self.proxy_obj = ProxyPool()
        self.proxies = random.choice(self.proxy_obj.get_xici())
        self.url_list = []
        self.retry_count = 5
        self.timeout = 80
        self.encode_type = "utf-8"
        self.sleep_min = 1
        self.sleep_max = 3
        self.csv_save_basic_path = r"G:\scielo_20190328"
        self.file_name = os.path.join(self.csv_save_basic_path, 'scielo2.csv')
        self.line_count = 0

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
            return
        for i in range(1, 15):
            js = "var q=document.documentElement.scrollTop={}".format(i*3000)
            driver.execute_script(js)
            time.sleep(2)
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
                print("二级页面请求失败")
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
            print("二级页面解析失败")
            return False
        self.test_third_page(url, journal_name, p_lock, self.retry_count)

    def test_third_page(self, url, journal_name, p_lock, retry_count):
        try:
            resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
        except Exception as e:
            print(e)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            if retry_count == 0:
                print("三级页面请求失败")
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
            print("三级页面解析失败")
            return False
        t_lock = threading.Lock()
        for url in result_list:
            t = threading.Thread(target=self.test_fourth_page, args=(url, journal_name, p_lock, t_lock, self.retry_count))
            t.start()
            t.join()
        print("当前进程的所有线程执行完毕")

    def test_fourth_page(self, url, journal_name, p_lock, t_lock, retry_count):
        print("当前线程的pid:{},ppid:{}".format(os.getpid(), os.getppid()))
        if ("2015" not in url) and ("2016" not in url) and ("2017" not in url) and ("2018" not in url) and ("2019" not in url):
            print("此页面期刊日期过期")
            return False
        try:
            resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
            print("四级页面请求的url:", url)
        except Exception as e:
            print(e)
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            if retry_count == 0:
                print("四级页面请求失败")
                return False
            self.test_fourth_page(url, journal_name, p_lock, t_lock, retry_count-1)
        else:
            resp.encoding = self.encode_type
            page_html = resp.text
            self.parse_fourth_page(page_html, journal_name, p_lock, t_lock)

    def parse_fourth_page(self, page_html, journal_name, p_lock, t_lock):
        result_list = []
        result_ls = re.findall(r"[a-zA-z]+://[^\s]*", page_html)
        for i in result_ls:
            if "arttext" in i:
                result_list.append(i.replace("\">text", "").replace("amp;", ""))
        print("四级页面请求结果：", result_list)
        del_email_ls = re.findall(r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", page_html)
        if del_email_ls:
            del_email = del_email_ls[0]
        else:
            del_email = "i_am_test_email"
        if not result_list:
            print("四级页面解析失败")
            return False
        print("要删除的邮箱：", del_email)
        self.test_detail_page(result_list, journal_name, p_lock, t_lock, self.retry_count, del_email)

    def test_detail_page(self, result_list, journal_name, p_lock, t_lock, retry_count, del_email):
        for url in result_list:
            print("详情页请求的url:", url)
            if (("2015" not in url) and ("2016" not in url) and ("2017" not in url) and ("2018" not in url) and ("2019" not in url)) or (url[-4:] == ".pdf"):
                print(url)
                continue
            time.sleep(random.randint(self.sleep_min, self.sleep_max))
            try:
                resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
            except Exception as e:
                print(e)
                time.sleep(random.randint(self.sleep_min, self.sleep_max))
                if retry_count == 0:
                    print("详情页面请求失败url:{}".format(url))
                    continue
                self.test_detail_page(result_list, journal_name, p_lock, t_lock, retry_count - 1, del_email)
            else:
                resp.encoding = self.encode_type
                page_html = resp.text
                self.callback(url, page_html, journal_name, p_lock, t_lock, del_email)

    def callback(self, url, page_html, journal_name, p_lock, t_lock, del_email):
        result_ls = []
        author_ls = []
        html = etree.HTML(page_html)
        if not html:
            print("调了一天了，好不容易弄好了，玩我呢$$")
            print("详情页数据采集失败url:", url)
            return False
        result_list1 = html.xpath('//*[@id="s1-front"]/div[2]//p/span[1]/text()')
        result_list2 = html.xpath('//*[@id="article-front"]/div[3]//p/span/text()')
        result_list3 = html.xpath('//*[@id="article-front"]/div[2]//p/span/text()')
        result_list4 = html.xpath('/html/body/div[1]/div[2]/div[2]/font/p[5]//text()')
        result_list5 = html.xpath('/html/body/div[1]/div[2]/div[2]/font/p[4]//text()')
        result_list6 = html.xpath('/html/body/div/div[2]/div[2]/p[6]/strong/font//text()')
        result_list7 = html.xpath('/html/body/div[1]/div[2]/div[2]/p[7]/font/b//text()')
        result_list8 = html.xpath('/html/body/div[1]/div[2]/div[2]/p[8]/font/b//text()')
        result_list9 = html.xpath('/html/body/div[1]/div[2]/div[2]/p[6]/font/b//text()')
        result_list10 = html.xpath('//*[@id="article-front"]/div[4]//text()')
        result_list11 = html.xpath('/html/body/div[1]/div[2]/div[2]/font/p[5]//text()')
        result_list12 = html.xpath('/html/body/div[1]/div[2]/div[2]/p[8]/b/font//text()')
        result_list13 = html.xpath('//*[@id="article-front"]/div[3]//text()')
        result_list14 = html.xpath('/html/body/div[1]/div[2]/div[2]/font[2]/p[1]//text()')
        result_list15 = html.xpath('/html/body/div[1]/div[2]/div[2]/p[3]/b//text()')
        result_list16 = html.xpath('/html/body/div[1]/div[2]/div[2]/p[2]/b//text()')
        flag = 0
        for i in range(1, 17):
            result_ls += eval("result_list{}".format(str(i)))
            if result_ls:
                for k in result_ls:
                    au = k.replace("\n", "").replace("\t", "").replace("\xa0", "").strip()
                    if len(au) >= 3:
                        author_ls.append(au)
                self.get_info(url, page_html, journal_name, author_ls, p_lock, t_lock, del_email)
                flag = 1
                break
        if flag == 0:
            print("详情页获取信息失败>>>url:{}".format(url))

    def get_info(self, url, page_html, journal_name, author_ls, p_lock, t_lock, del_email):
        email_ls = []
        pattern = re.compile(r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", re.S)

        # 这里还是要处理一下(去重不能用集合呀，顺序不能保证)
        result_ls = list(set(re.findall(pattern, page_html)))
        for i in result_ls:
            if del_email in i:
                result_ls.remove(i)
        for i in result_ls:
            if i not in email_ls:
                email_ls.append(i)
        count_e = len(email_ls)
        flag = 0
        if count_e == 1:
            print("执行count_e=1")
            index_e = result_ls[0].find("@")
            au = result_ls[0][index_e - 4:index_e]
            email = email_ls[0].strip()
            for a in author_ls:
                if au.upper() in a.upper():
                    author = a.replace(";", "").replace(",", "").replace("‘", "").replace("’", "").replace("“", "").replace("”", "").strip()
                    info = [self.classify, journal_name, author, email]
                    self.save_to_csv(info, p_lock, t_lock)
                    flag = 1
            if flag == 0:
                author = author_ls[0]
                info = [self.classify, journal_name, author, email]
                self.save_to_csv(info, p_lock, t_lock)
        elif count_e > 1:
            print("执行count_e>1")
            if len(author_ls) <= 1:
                author_ls = author_ls[0].split(";")
                for i in range(count_e):
                    try:
                        email = email_ls[i].strip()
                        author = author_ls[i].replace(";", "").replace(",", "").replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("*", "").strip()
                    except IndexError:
                        continue
                    info = [self.classify, journal_name, author, email]
                    self.save_to_csv(info, p_lock, t_lock)
            elif len(author_ls) > 1:
                for e in email_ls:
                    index_e = e.find("@")
                    au = e[index_e-3:index_e]
                    email = e.strip()
                    for a in author_ls:
                        if au.upper() in a.upper():
                            author = a.replace(";", "").replace(",", "").replace("‘", "").replace("’", "").replace("“", "").replace("”", "").strip()
                            info = [self.classify, journal_name, author, email]
                            self.save_to_csv(info, p_lock, t_lock)
                            author_ls.remove(a)
                            author_ls = author_ls.copy()
                            break



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
    print("此次爬虫任务已完成")