# -*- coding: utf-8 -*-
"""
Author:doom
datetime:2019.2.26
email:408575225@qq.com
github:doom2020
function: use requests model get new journal
comment:if you update my code,please update comment as too,thanks

"""

import requests
import re
import random
import time
import csv
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from get_user_agent import get_user_agent
from proxy_pool import *
from myLogger import LogHelper
import multiprocessing
import os


def get_page_timeout_error():
    """this function:deal with get page timeout error"""
    pass


def get_page_code_abnormal():
    """this function:deal with get page code abnormal"""
    pass


def save_info2_csv(ls, lock):
    """this function:get info save to csv file"""
    lock.acquire()
    with open(r'C:\Users\Administrator\Desktop\2019_3_6_8.csv', 'a', newline="", encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(ls)
    lock.release()


# used 2018all,2017.5.6,2017.5.5(just new journal)
def get_one_page(summary_title, title_href_list, lock):
    """this function get info from detail page"""
    headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
    for url in title_href_list:
        time.sleep(random.randint(1, 2))
    # url = "https://www.omicsonline.org/open-access/nitrogen-sources-and-levels-improve-crop-productivity-and-nitrogen-use-efficiency-in-three-wheat-cultivars-2329-8863-1000405-106909.html"
    #     headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        try:
            resp = requests.get(url, headers=headers, timeout=15)
        except Exception as e:
            print(e)
            print("url:{}request page fail".format(url))
            time.sleep(1)
            continue
        else:
            print(resp.status_code)
            resp.encoding = "utf-8"
            page_html = resp.text
            # use xpath match
            html = etree.HTML(page_html)
            # match title
            '/html/body/div[3]/div/div/div/div/div[2]/div[1]/h1/text()'
            # format1:2018
            title = ",".join(html.xpath('//article[@class="full-text"]//h1//text()'))
            # match author
            # format1:2018
            author = ",".join(html.xpath('//article[@class="full-text"]/dl/dt/a/text()'))
            # match position
            # format1:2018
            position = ",".join(html.xpath('//article/dl//dd/text()'))
            '/html/body/div[3]/div/div/div/div/div[1]/div[1]/article/dl'
            '/html/body/div[3]/div/div/div/div/div[1]/div[1]/article/dl'
            '//*[@id="a1"]'
            # position = html.xpath('//*[@id="a1"]//text()')
            # match email
            '//article[@class="full-text"]/div/a[3]'
            '/html/body/div[3]/div/div/div/div/div[1]/div[1]/article/div/a[2]'
            # format1:2018
            email = ",".join(html.xpath('//article/div/a[last()]/@title'))
            # save to dict
            ls = [summary_title, title, author, position, email]
            print(ls)
            if ls[-1]:
                save_info2_csv(ls, lock)


def get_page_title_href_list(url, lock, get_user_agent):
    """get all url form show_page (third child page)"""
    print("当前进程pid:{},当前进程ppid:{}".format(os.getpid(), os.getppid()))
    """此方法提取目录展示页的标题url"""
    headers = random.choice(get_user_agent)
    socks5_proxy = '101.251.200.133:45990'
    proxies = {
        'http': 'socks5://' + socks5_proxy,
        'https': 'socks5://' + socks5_proxy
    }
    time.sleep(random.randint(1, 2))
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=15)
    except Exception as e:
        print(e)
        print("url:{}request page fail".format(url))
    else:
        print(resp.status_code)
        resp.encoding = "utf-8"
        page_html = resp.text
        # use 're' model match summary
        pattern_summary_title = re.compile('<title>(.*?)</title>')
        summary_title = re.findall(pattern_summary_title, page_html)[0]
        print(summary_title)
        print(summary_title[-1])
        # use 're' model match title url
        pattern_title_href = re.compile('<strong>.*?<a href="(.*?)"')
        title_href_list = re.findall(pattern_title_href, page_html)[1:-1]
        print(title_href_list)
        get_one_page(summary_title, title_href_list, lock)


def get_all_href():
    """此方法获取当前期刊类型的所有期刊url"""
    # 初始化href列表
    vaild_href_list = []
    print("开始调用倒数第二个函数")
    classify_href_list = get_archive()[-60:]
    for url_href in classify_href_list:
        for url_h in url_href:
            headers = random.choice(get_user_agent)
            try:
                resp = requests.get(url_h, headers=headers, proxies=None, timeout=30)
                print(resp.status_code)
                print(url_href)
            except Exception as e:
                print(e)
                print("url:{}.请求页面失败".format(url_href))
                time.sleep(random.randint(2, 4))
                continue
            else:
                print(resp.status_code)
                time.sleep(random.randint(1, 2))
                resp.encoding = "utf-8"
                page_html = resp.text
                # 使用xpath进行匹配
                html = etree.HTML(page_html)
                all_href_list = html.xpath('//div[@class="card mb-3"]//a/@href')
                for href in all_href_list:
                    # 剔除href以"php"结尾的文件
                    if href[-4:] == "html":
                        vaild_href_list.append(href)
                print(vaild_href_list)
    return vaild_href_list


def get_archive():
    """this function:get has 'archive' element' href (first child page)"""
    # init href list
    valid_classify_list = []
    all_classify_href_list = get_classify_href_list()
    num = 0
    count = len(all_classify_href_list)
    headers = random.choice(get_user_agent)
    socks5_proxy = '101.251.200.133:45990'
    proxies = {
        'http': 'socks5://' + socks5_proxy,
        'https': 'socks5://' + socks5_proxy
    }
    for classify_url in all_classify_href_list:
        try:
            resp = requests.get(classify_url, headers=headers, proxies=proxies, timeout=15)
        except Exception as e:
            print(e)
        else:
            resp.encoding = "utf-8"
            page_html = resp.text
            # use xpath match
            html = etree.HTML(page_html)
            archive = html.xpath('//nav[@class="nav"]/a[last()]/@href')
            print(archive)
            if archive:
                valid_classify_list.append(archive)
                print("get valid url include 'archive' element:", archive)
            else:
                print("this url page not found archive")
                print("url:{}is not valid".format(classify_url))
            num += 1
            rate = float(num / count) * 100
            print("completed rate:{}%".format(rate))
    print("valid url count:", len(valid_classify_list))
    return valid_classify_list


def get_classify_href_list():
    """this function:get all classify journal url (parent page)"""
    # init href list
    all_classify_href_list = []
    # setting user-agent
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11")
    # setting not load image(False)
    dcap["phantomjs.page.settings.loadImages"] = False
    # driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.set_page_load_timeout(200)
    url = "https://www.omicsonline.org/scientific-journals.php"
    try:
        driver.get(url)
    except Exception as e:
        print("request timeout:", e)
        driver.quit()
        return
    js1 = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js1)
    js2 = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js2)
    time.sleep(5)
    page_html = driver.page_source
    time.sleep(2)
    driver.quit()
    # use 're' model match all classify url
    pattern_classify = re.compile('<a class="nav-link dark-golden-rod-before col-6" href="(.*?)".*?</a>', re.S)
    classify_href_list = re.findall(pattern_classify, page_html)
    # delete the "php" href
    for classify_href in classify_href_list:
        if classify_href[:27] == "https://www.omicsonline.org" or classify_href[-3:] == "php":
            all_classify_href_list.append(classify_href)
            print(classify_href)
    print("href count:", len(all_classify_href_list))
    return all_classify_href_list


if __name__ == "__main__":
    # process lock
    lock = multiprocessing.Lock()
    # callback user-agent
    get_user_agent = get_user_agent()
    href_list = get_all_href()
    for url in href_list:
        p = multiprocessing.Process(target=get_page_title_href_list, args=(url, lock, get_user_agent))
        p.start()
        p.join()
    print("all process over")