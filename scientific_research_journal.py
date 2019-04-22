"""
author:doom
email:408575225@qq.com
datetime:20190419
github:doom2020
function:get scientific research journal(only to get has image_email)
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
from lxml import etree
import cv2
import numpy as np
from myLogger import LogHelper #(Notice:use "logger" instead of "print()" in order to easy find the code problem)


class ScientificResearchJournal:
    def __init__(self):
        self.home_url = "https://www.scirp.org/"
        self.chrome_request_max_time = 80
        self.chrome_request_min_time = 50
        self.headers_list = get_user_agent()
        self.proxy_obj = ProxyPool()
        self.proxy_list = self.proxy_obj.get_kuai()
        self.create_process_max_time = 3
        self.create_process_min_time = 1
        # requests get page fail retry count
        self.retry_count = 5
        self.sleep_time_max = 3
        self.sleep_time_min = 1
        self.scroll_length = 700
        self.data_type = "Journal"
        self.begin_page = 1
        self.timeout = 65
        self.encode_type = "utf-8"
        self.request_page_type = "https"
        self.request_image_type = "http"
        self.img_save_basic_path = r"G:\scientific_research\email_img_update3"
        self.img_type = ".png"
        self.csv_save_basic_path = r"G:\scientific_research\csv_file_update3"
        self.csv_type = ".csv"
        self.file_name = os.path.join(self.csv_save_basic_path, ("scientific_research" + self.csv_type))
        self.line_count = 0
        # image filter
        self.threshold = 140
        self.img_max_pixel = 255
        self.img_min_pixel = 0
        self.method_count = 3
        self.info_list = []
        self.info_count = 0

    def get_journal_name_page(self):
        url = self.home_url
        # setting http proxies
        # the http proxies is invalid(you can try once again)
        # proxy_get = random.choice(self.proxy_list)
        headers_get = random.choice(self.headers_list)
        # setting socks5 proxies
        socks5_proxy = '39.96.38.189:45990'
        chrome_option = webdriver.ChromeOptions()
        # just execute not show chrome,in order to improve the process
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-gpu')
        proxy = "--proxy-server=socks5://" + socks5_proxy
        user_agent = "user-agent=" + headers_get["User-Agent"]
        chrome_option.add_argument(proxy)
        chrome_option.add_argument(user_agent)
        driver = webdriver.Chrome(chrome_options=chrome_option)
        driver.set_page_load_timeout(random.randint(self.chrome_request_min_time, self.chrome_request_max_time))
        try:
            driver.get(url)
        except TimeoutError:
            print("home page request fail")
            driver.quit()
        time.sleep(random.randint(self.sleep_time_min, self.sleep_time_max))
        try:
            driver.find_element_by_xpath('//*[@id="header"]/div[3]/ul/li[3]/a').click()
        except Exception as e:
            print(e)
            print("element find fail")
            driver.quit()
        time.sleep(self.sleep_time_max)
        page_html = driver.page_source
        # print(page_html)
        driver.quit()
        self.parse_journal_name_page(page_html)

    def parse_journal_name_page(self, page_html):
        html = etree.HTML(page_html)
        journal_name_href_list = html.xpath('//*[@id="txtHintj"]/div[2]//ul//li/a/@href')
        journal_name_title_list = html.xpath('//*[@id="txtHintj"]/div[2]//ul//li/a/@title')
        title_count = len(journal_name_title_list)
        href_count = len(journal_name_href_list)
        if journal_name_href_list and journal_name_title_list and (title_count == href_count):
            # create many process
            self.create_process_pool(journal_name_href_list, journal_name_title_list)
        else:
            print("title number:{},href number:{},{}".format(title_count, href_count, "title_count != href_count" if title_count != href_count else "title_count == href_count"))

    def create_process_pool(self, journal_name_href_list, journal_name_title_list):
        logger_help = LogHelper()
        logger_help.writeLog(journal_name_title_list, level="info")
        logger_help.writeLog(journal_name_href_list, level="info")
        p = multiprocessing.Pool()
        for href, title in zip(journal_name_href_list, journal_name_title_list):
            tuple_one = (href, title)
            p.apply_async(func=self.get_second_page, args=(tuple_one, self.retry_count), callback=self.save2csv)
            logger_help.writeLog("the current journal name>>>{},href>>>{}".format(title, href), level="info")
            time.sleep(random.randint(self.create_process_min_time, self.create_process_max_time))
        p.close()
        p.join()
        logger_help.removeLog()

    def get_second_page(self, tuple_one, retry_count):
        journal_name = tuple_one[1].strip()
        url = tuple_one[0]
        headers_get = random.choice(self.headers_list)
        # setting socks5 proxies
        socks5_proxy = '39.96.38.189:45990'
        chrome_option = webdriver.ChromeOptions()
        # just execute not show chrome,in order to improve the process
        chrome_option.add_argument('--headless')
        chrome_option.add_argument('--disable-gpu')
        proxy = "--proxy-server=socks5://" + socks5_proxy
        user_agent = "user-agent=" + headers_get["User-Agent"]
        chrome_option.add_argument(proxy)
        chrome_option.add_argument(user_agent)
        driver = webdriver.Chrome(chrome_options=chrome_option)
        driver.set_page_load_timeout(random.randint(self.chrome_request_min_time, self.chrome_request_max_time))
        try:
            driver.get(url)
        except TimeoutError:
            if retry_count == 0:
                # here suggest use logger writer abnormal url
                print("the second page html request fail >>>url:{}".format(url))
                driver.quit()
            else:
                self.get_second_page(tuple_one, retry_count-1)
        time.sleep(self.sleep_time_min)
        # notice:this scroll in frame,so need switch to frame before execute js
        driver.switch_to.frame("main")
        for i in range(1, 5):
            js = "var q=document.documentElement.scrollTop={}".format(i * self.scroll_length)
            driver.execute_script(js)
            time.sleep(random.randint(self.sleep_time_min, self.sleep_time_max))
        time.sleep(self.sleep_time_max)
        page_html = driver.page_source
        # print(page_html)
        driver.switch_to.default_content()
        driver.quit()
        retry_count = self.retry_count
        self.parse_second_page(page_html, journal_name, retry_count)
        return self.info_list

    def parse_second_page(self, page_html, journal_name, retry_count):
        html = etree.HTML(page_html)
        result_ls = html.xpath('//*[@id="JournalInfor_AspNetPager"]/a[last()]/@href')
        if result_ls:
            self.get_third_page(result_ls, journal_name, retry_count)
        else:
            return False

    def get_third_page(self, result_ls, journal_name, retry_count):
        split_url = result_ls[0][:-1]
        basic_url = self.home_url + self.data_type + "/" + split_url
        page_count = int(result_ls[0][-1])
        for i in range(self.begin_page, page_count + 1):
            url = basic_url + str(i)
            headers = random.choice(self.headers_list)
            proxies = random.choice(self.proxy_list)
            try:
                resp = requests.get(url, headers=headers, proxies=proxies, timeout=self.timeout)
            except Exception as e:
                print(e)
                time.sleep(random.randint(self.sleep_time_min, self.sleep_time_max))
                if retry_count == 0:
                    print("detail summary page html request fail")
                    return False
                else:
                    self.get_third_page(url, journal_name, retry_count-1)
            else:
                resp.encoding = self.encode_type
                page_html = resp.text
                retry_count = self.retry_count
                self.parse_third_page(page_html, journal_name, retry_count)

    def parse_third_page(self, page_html, journal_name, retry_count):
        html = etree.HTML(page_html)
        result_ls_href = html.xpath('//*[@id="JournalInfor_UpdatePanel1"]/div[2]//ul/p[3]/a[3]/@href')
        self.request_detail_page(result_ls_href, journal_name, retry_count)

    def request_detail_page(self, result_ls_href, journal_name, retry_count):
        for i in result_ls_href:
            if i[-4:] != ".htm":
                continue
            url = self.request_page_type + ":" + i
            headers = random.choice(self.headers_list)
            proxies = random.choice(self.proxy_list)
            try:
                resp = requests.get(url, headers=headers, proxies=proxies, timeout=self.timeout)
            except Exception as e:
                print(e)
                time.sleep(random.randint(self.sleep_time_min, self.sleep_time_max))
                if retry_count == 0:
                    print("detail page html request fail")
                    print("detail page url:{}".format(url))
                    return False
                else:
                    self.request_detail_page(result_ls_href, journal_name, retry_count - 1)
            else:
                resp.encoding = self.encode_type
                page_html = resp.text
                retry_count = self.retry_count
                self.parse_detail_page(page_html, journal_name, retry_count)

    def parse_detail_page(self, page_html, journal_name, retry_count):
        html = etree.HTML(page_html)
        title_ls = html.xpath('//*[@id="con_one_1"]/div[1]/div/div[1]/p[2]/text()')
        if title_ls:
            title = title_ls[0].replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("\t", "").replace("\n", "").strip()
        else:
            title = "get_title_fail"
        author_list = html.xpath('//*[@id="con_one_1"]/div[1]/div/div[1]/p[3]//text()')
        if not author_list:
            return False
        author_ls = "".join(author_list).split(",")
        # 此处两种情况：图片邮箱，或者a标签邮箱
        email_re_ls = re.findall(r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", page_html)
        if email_re_ls:
            email_ls = list(set(email_re_ls))
            self.sort_info2(email_ls, journal_name, title, author_ls)
        else:
            email_src_ls = re.findall(r'<p class="cs_address">.*?<img src="(.*?)"', page_html)
            if email_src_ls:
                flag = 0
                for i in email_src_ls:
                    if "x1" in i:
                        email_src = i
                        self.get_img(email_src, journal_name, title, author_ls, retry_count)
                        flag = 1
                        break
                if flag == 0:
                    return False
            else:
                return False

    def get_img(self, email_src, journal_name, title, author_ls, retry_count):
        if email_src[:4] == "http":
            url = email_src
        else:
            url = self.request_image_type + ":" + email_src
        print("the email image url：{}".format(url))
        headers = random.choice(self.headers_list)
        proxies = random.choice(self.proxy_list)
        try:
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=self.timeout)
        except Exception as e:
            print(e)
            time.sleep(random.randint(self.sleep_time_min, self.sleep_time_max))
            if retry_count == 0:
                print("email image html request fail")
                return False
            else:
                self.get_img(email_src, journal_name, title, author_ls, retry_count - 1)
        else:
            resp.encoding = self.encode_type
            page_html = resp.content
            self.img2save(page_html, journal_name, title, author_ls)

    def img2save(self, page_html, journal_name, title, author_ls):
        md5 = hashlib.md5()
        md5.update(page_html)
        img_name = md5.hexdigest() + self.img_type
        file = os.path.join(self.img_save_basic_path, img_name)
        with open(file, 'wb') as fw:
            fw.write(page_html)
        print("image save success")
        print("the image name:", img_name)
        time.sleep(self.sleep_time_min)
        self.img_to_text_callback(file, journal_name, title, author_ls)

    def img_to_text_callback(self, file, journal_name, title, author_ls):
        print("start execute img_to_text_callback function")
        # 第一种方法直接识别，第二种方法，二值化处理，第三种方法，使用opencv
        flag = 0
        for i in range(1, self.method_count + 1):
            result = eval('self.img_to_text{}(file, journal_name, title, author_ls)'.format(i))
            print("IS OK?>>>>", bool(result))
            if result:
                flag = i
                print("the{}method recognize success".format(flag))
                break
        if flag == 0:
            print("email recognize fail")
            return False

    def img_to_text1(self, file, journal_name, title, author_ls):
        print("start execute img_to_text1 function")
        image = Image.open(file)
        result = tesserocr.image_to_text(image)
        if "@" not in result:
            return False
        else:
            self.sort_info(result, journal_name, title, author_ls)
            return True

    def img_to_text2(self, file, journal_name, title, author_ls):
        print("start execute img_to_text2 function")
        image = Image.open(file)
        image = image.convert("L")
        threshold = self.threshold
        table = []
        for i in range(self.img_max_pixel + 1):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, "1")
        result = tesserocr.image_to_text(image)
        if "@" not in result:
            return False
        else:
            self.sort_info(result, journal_name, title, author_ls)
            return True

    def img_to_text3(self, file, journal_name, title, author_ls):
        print("start execute img_to_text3 function")
        image = cv2.imread(file)
        image_np = np.array(image)
        new_img = np.where(image_np > self.threshold, self.img_max_pixel, self.img_min_pixel)
        md5 = hashlib.md5()
        md5.update("".join(author_ls))
        img_name = md5.hexdigest() + self.img_type + title
        img_file = os.path.join(self.img_save_basic_path, img_name)
        cv2.imwrite(img_file, new_img)
        result = self.img_to_text2(img_file, journal_name, title, author_ls)
        if result:
            return True
        else:
            return False

    def sort_info(self, result, journal_name, title, author_ls):
        print("the current get journal name is:{}".format(journal_name))
        pattern = re.compile(r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", re.S)
        email_ls = re.findall(pattern, result.replace("*", ""))
        if not email_ls:
            return False
        else:
            for a in author_ls:
                if len(a) < 3:
                    author_ls.remove(a)
                    author_ls = author_ls.copy()
            email_count = len(email_ls)
            if email_count == 1:
                email_filter_ls = email_ls[0].split(".")
                email_before = ".".join(email_filter_ls[:-1])
                email_after = email_filter_ls[-1]
                if email_after[0] == "c" and email_after[-1] == "m":
                    email = email_before + ".com"
                else:
                    email = email_ls[0]
                index_e = email.find("@")
                au_part = email[index_e-3:index_e]
                flag = 0
                for a in author_ls:
                    if au_part.upper() in a.upper():
                        author = a.replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("1", "").replace("2", "").replace("*", "").strip()
                        one_info = [journal_name, title, author, email]
                        print("one_info:{}".format(one_info))
                        self.info_list.append(one_info)
                        self.info_count += 1
                        print("current has{} data".format(self.info_count))
                        flag = 1
                        break
                if flag == 0:
                    author = author_ls[0].replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("1", "").replace("2", "").replace("*", "").strip()
                    one_info = [journal_name, title, author, email]
                    print("one_info:{}".format(one_info))
                    self.info_list.append(one_info)
                    self.info_count += 1
                    print("current has{} data".format(self.info_count))
            elif email_count > 1:
                for e in email_ls:
                    index_e = e.find("@")
                    au_part = e[index_e-3:index_e]
                    for a in author_ls:
                        if au_part.upper() in a.upper():
                            try:
                                author = a.replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("1", "").replace("2", "").replace("*", "").strip()
                                email_filter_ls = e.split(".")
                                email_before = ".".join(email_filter_ls[:-1])
                                email_after = email_filter_ls[-1]
                                if email_after[0] == "c" and email_after[-1] == "m":
                                    email = email_before + ".com"
                                else:
                                    email = e
                            except IndexError:
                                continue
                            one_info = [journal_name, title, author, email]
                            print("one_info:{}".format(one_info))
                            self.info_list.append(one_info)
                            self.info_count += 1
                            print("current has{} data".format(self.info_count))
                            author_ls.remove(a)
                            author_ls = author_ls.copy()
                            break

    def sort_info2(self, email_ls, journal_name, title, author_ls):
        count_e = len(email_ls)
        if count_e == 1:
            email = email_ls[0]
            index_e = email.find("@")
            au = email[index_e-3:index_e]
            flag = 0
            for a in author_ls:
                if au.upper() in a.upper():
                    author = a.replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("1", "").replace("2", "").replace("*", "").strip()
                    one_info = [journal_name, title, author, email]
                    print("one_info:{}".format(one_info))
                    self.info_list.append(one_info)
                    self.info_count += 1
                    print("current has{} data".format(self.info_count))
                    flag = 1
                    break
            if flag == 0:
                author = author_ls[0].replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("1", "").replace("2", "").replace("*", "").strip()
                one_info = [journal_name, title, author, email]
                print("one_info:{}".format(one_info))
                self.info_list.append(one_info)
                self.info_count += 1
                print("current has{} data".format(self.info_count))
        elif count_e > 1:
            for a in author_ls:
                if len(a) < 3:
                    author_ls.remove(a)
                    author_ls = author_ls.copy()
            for e in email_ls:
                index_e = e.find("@")
                au = e[index_e-3:index_e]
                for a in author_ls:
                    if au.upper() in a.upper():
                        author = a.replace("‘", "").replace("’", "").replace("“", "").replace("”", "").replace("1", "").replace("2", "").replace("*", "").strip()
                        email = e
                        one_info = [journal_name, title, author, email]
                        print("one_info:{}".format(one_info))
                        self.info_list.append(one_info)
                        self.info_count += 1
                        print("current has{} data".format(self.info_count))
                        author_ls.remove(a)
                        author_ls = author_ls.copy()
                        break


    def save2csv(self, info_list):
        print("start writer the data")
        print("data：{}".format(info_list))
        # first_line = ["journal_name", "title", "author", "email"]
        with open(self.file_name, "a", newline="", encoding="utf-8", errors='ignore') as fw:
            writer = csv.writer(fw)
            # writer.writerow(first_line)
            writer.writerows(info_list)
        print("writer data finish")


if __name__ == "__main__":
    journal = ScientificResearchJournal()
    time_begin = time.time()
    journal.get_journal_name_page()
    print("此次爬虫任务已完成")
    time_end = time.time()
    summary_use_time = (time_end - time_begin) / (60*60)
    print("总共时长:{:.2f}小时".format(summary_use_time))