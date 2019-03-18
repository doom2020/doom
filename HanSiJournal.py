"""
author:doom
email:408575225@qq.com
datetime:20190315
github:doom2020
function:get han si journal (only the new journal for 2016-2019 year)
comment:if you update my code ,please update comment as too,thanks

"""
import csv
import requests
import re
from selenium import webdriver
from get_user_agent import get_user_agent
import random
import time
import os
import tesserocr
from PIL import Image
import hashlib
import multiprocessing
from proxy_pool import ProxyPool
import threading
from lxml import etree


class HanSiJournal:
    # 外部类属性
    # 1.创建User-Agent池
    user_agent_list = get_user_agent()
    # 1.创建Proxies池
    proxy_obj = ProxyPool()
    proxies_list = proxy_obj.get_kuai()
    # 3.请求超时时间设定
    timeout = 30
    # 4.设定请求失败次数
    retry_count = 5

    def __init__(self):
        # 外部类对象的属性
        pass

    @classmethod
    def deal_with_request_abnormal(cls):  # 外部类方法
        """异常处理方法"""
        pass

    @classmethod
    def func1(cls):
        pass

    @classmethod
    def func2(cls):
        pass

    def example(self):  # 外部类对象方法
        pass

    # 心理学进展(内部类)
    class AdvancesInPsychology:
        # 'https://www.hanspub.org/journal/JouCons.aspx?ShortName=AP&page=2'
        def __init__(self):
            self.basic_url = "https://www.hanspub.org/journal/JouCons.aspx?ShortName=AP&page="
            self.begin_page_num = 1
            self.end_page_num = 49
            self.encode_type = "utf-8"
            self.sleep_min = 1
            self.sleep_max = 4
            self.detail_basic_url = "https:"
            self.classify = "Advances_in_Psychology"
            self.img_basic_url = "http:"
            self.img_save_basic_path = r"C:\Users\Administrator\Desktop\email_image"
            self.img_type = ".png"
            self.csv_save_basic_path = r"C:\Users\Administrator\Desktop\info"
            self.csv_type = ".csv"
            self.line_count = 0
            self.email_type = "qq.com"
            # 不选择在这里调用User-Agent和Proxies
            self.headers = random.choice(HanSiJournal.user_agent_list)
            self.proxies = random.choice(HanSiJournal.proxies_list)

        def create_many_process(self):
            retry_count = HanSiJournal.retry_count
            p_lock = multiprocessing.Lock()
            for page_num in range(self.begin_page_num + 17, self.end_page_num+1):
                url = self.basic_url + str(page_num)
                p = multiprocessing.Process(target=self.get_page_url, args=(url, p_lock, retry_count, page_num))
                p.start()
                p.join()
            print("所有进程完成")

        def create_many_threading(self, valid_list, p_lock, page_num):
            t_lock = threading.Lock()
            for result in valid_list:
                url = self.detail_basic_url + result
                # url = result
                t = threading.Thread(target=self.get_detail_info, args=(url, p_lock, t_lock, page_num))
                t.start()
                t.join()
            print("当前线程已完成")

        def get_page_url(self, url, p_lock, retry_count, page_num):
            print("当前进程pid:{},ppid{}".format(os.getpid(), os.getppid()))
            # # 调用User-Agent pool
            # self.headers = random.choice(HanSiJournal.user_agent_list)
            # # 调用Proxies pool
            # self.proxies = random.choice(HanSiJournal.proxies_list)
            try:
                resp = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=HanSiJournal.timeout)
            except Exception as e:
                print(e)
                time.sleep(random.randint(self.sleep_min, self.sleep_max))
                if retry_count == 0:
                    errmsg = "目录页url:{}请求页面失败".format(url)
                    print(errmsg)
                    return False
                self.get_page_url(url, p_lock, retry_count-1, page_num)
            else:
                resp.encoding = self.encode_type
                page_html = resp.text
                # print(page_html)
                html = etree.HTML(page_html)
                result_list = html.xpath('//*[@id="ctl00_ContentPlaceHolder1_zxwz"]/div//ul/li[5]/a[3]/@href')
                valid_list = []
                for i in result_list:
                    if i[-4:] == ".htm":
                        valid_list.append(i)
                print("get_page_url 函数执行完成")
                # return result_list
                self.create_many_threading(valid_list, p_lock, page_num)

        def get_detail_info(self, url, p_lock, t_lock, page_num):
            print("当前线程pid:{},ppid{}".format(os.getpid(), os.getppid()))
            # VPN socks5代理ip和端口
            socks5_proxy = '39.96.38.189:45990'
            # 修改selenium请求设置
            chrome_option = webdriver.ChromeOptions()
            chrome_option.add_argument('--headless')
            chrome_option.add_argument('--disable-gpu')
            proxy = "--proxy-server=socks5://" + socks5_proxy
            user_agent = "user-agent=" + self.headers["User-Agent"]
            chrome_option.add_argument(proxy)
            chrome_option.add_argument(user_agent)
            driver = webdriver.Chrome(chrome_options=chrome_option)
            driver.set_page_load_timeout(random.randint(50, 80))
            try:
                driver.get(url)
            except Exception as e:
                print("requests timeout:", e)
                errmsg = "详情页url:{}请求失败".format(url)
                print(errmsg)
                driver.quit()
                return False
            js1 = "var q=document.documentElement.scrollTop=10000"
            driver.execute_script(js1)
            js2 = "var q=document.documentElement.scrollTop=100"
            driver.execute_script(js2)
            time.sleep(6)
            page_html = driver.page_source
            # print(page_html)
            time.sleep(1)
            driver.quit()
            print("get_detail_info 函数执行完成")
            self.parse_page_info(page_html, url, p_lock, t_lock, page_num)

        def parse_page_info(self, page_html, url, p_lock, t_lock, page_num):
            pattern_title_author_position = re.compile('<a.*?id="txtF1">(.*?)<sup>.*?<p>(.*?)</p>.*?<p>(.*?)</p>', re.S)
            pattern_email = re.compile('<p class="cs_address">.*?<img src="(.*?)".*?</p>', re.S)
            result_title_author_position_ls = re.findall(pattern_title_author_position, page_html)
            result_email_ls = re.findall(pattern_email, page_html)
            try:
                title = result_title_author_position_ls[0][0].strip()
                position = result_title_author_position_ls[0][-1].split(">")[-1].strip()
            except IndexError:
                title = "NA"
                position = "NA"
                try:
                    author = result_title_author_position_ls[0][1].split("<")[0].strip()
                    email_src = result_email_ls[0].strip()
                except IndexError:
                    errmsg_index = "url:{}页面信息抓取失败".format(url)
                    print(errmsg_index)
                    return False
                else:
                    one_info = [title, author, position, email_src]
                    print("个人信息:", one_info)
                    src_email = one_info[-1]
                    self.get_img(src_email, title, author, position, p_lock, t_lock, page_num)
            else:
                try:
                    author = result_title_author_position_ls[0][1].split("<")[0].strip()
                    email_src = result_email_ls[0].strip()
                except IndexError:
                    errmsg_index = "url:{}页面信息抓取失败".format(url)
                    print(errmsg_index)
                    return False
                else:
                    one_info = [title, author, position, email_src]
                    print("个人信息:", one_info)
                    src_email = one_info[-1]
                    self.get_img(src_email, title, author, position, p_lock, t_lock, page_num)

        def get_img(self, src_image, title, author, position, p_lock, t_lock, page_num):
            if src_image[:4] == "http":
                url = src_image
            else:
                url = self.img_basic_url + src_image
            # url = src_image
            resp = requests.get(url, headers=self.headers, proxies=self.proxies)
            resp.encoding = self.encode_type
            page_html = resp.content
            print("get_img 函数执行完成")
            self.img2save(page_html, title, author, position, p_lock, t_lock, page_num)

        def img2save(self, page_html, title, author, position, p_lock, t_lock, page_num):
            md5 = hashlib.md5()
            md5.update(page_html)
            img_name = md5.hexdigest() + self.img_type
            file = os.path.join(self.img_save_basic_path, img_name)
            with open(file, 'wb') as fw:
                fw.write(page_html)
            print("图片保存成功")
            print("图片名称:", img_name)
            print("img2save 函数执行完成")
            self.img2text(file, title, author, position, p_lock, t_lock, page_num)

        def img2text(self, file, title, author, position, p_lock, t_lock, page_num):
            image = Image.open(file)
            result = tesserocr.image_to_text(image).split(":")[-1].strip().replace("/", "").replace("\n", "").replace("\n\n", "").replace("\t", "").replace("”", "").replace("“", "").replace("|", "").replace("(", "")
            print("原始识别出来的邮箱:", result)
            try:
                index_e = result.index("@")
            except ValueError:
                print("图片识别失败")
                return False
            else:
                try:
                    if result[index_e + 1] == "q" or result[index_e + 2] == "q":
                        email = result[:index_e + 1] + self.email_type
                        print("处理后的邮箱:", email)
                        info = [self.classify, title, author, position, email]
                        if author and "@" in email:
                            print("写入csv中的信息是:", info)
                            self.info_save2csv(info, p_lock, t_lock, page_num)
                    else:
                        email = result
                        print("未经处理的邮箱:", email)
                        info = [self.classify, title, author, position, email]
                        if author and "@" in email:
                            print("写入csv中的信息是:", info)
                            self.info_save2csv(info, p_lock, t_lock, page_num)
                except IndexError:
                    print("图片异常")
                    return False

        def info_save2csv(self, info, p_lock, t_lock, page_num):
            file_name = self.classify + str(page_num) + self.csv_type
            csv_file = os.path.join(self.csv_save_basic_path, file_name)
            print("上进程锁")
            p_lock.acquire()
            print("上线程锁")
            t_lock.acquire()
            try:
                with open(csv_file, "a", newline="", encoding="gbk", errors='ignore') as fw:
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
            print("info_save2csv 函数执行完成")


if __name__ == "__main__":
    # 创建内部类实例
    psychology = HanSiJournal.AdvancesInPsychology()
    # 创建多进程(进程池下次在用吧)
    psychology.create_many_process()
    print("此次爬虫任务已完成")





