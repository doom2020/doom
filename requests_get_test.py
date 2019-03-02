# -*- coding: utf-8 -*-
"""
Author:doom
datetime:2019.2.26
email:408575225@qq.com
github:doom2020
function:requests test for old journal
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
import multiprocessing
import os


def save_info2_csv(ls):
    """this function: info save to csv file"""
    with open(r'C:\Users\Administrator\Desktop\2019_test.csv', 'a', newline="", encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(ls)

# this function is used the old journal
def get_one_page(url, user_agent_list):
    """this function:get detail page info"""
    print("process ppid:{},process pid:{}".format(os.getppid(), os.getpid()))
    socks5_proxy = '101.251.200.133:45990'
    proxies = {
        'http': 'socks5://' + socks5_proxy,
        'https': 'socks5://' + socks5_proxy
    }
    headers = random.choice(user_agent_list)
    try:
        resp = requests.get(url, headers=headers,  proxies=proxies, timeout=15)
    except Exception as e:
        print(e)
        print("url:{}request page fail".format(url))
        time.sleep(1)
    else:
        print(resp.status_code)
        time.sleep(5)
        resp.encoding = "utf-8"
        page_html = resp.text
        print(page_html)
        html = etree.HTML(page_html)
        # match title
        title = ",".join(html.xpath('//h1[@class="fulltext_h1heading margin-t-0"]//text()')).replace("\n", " ")
        # match author
        author_list = html.xpath('//div[@class="row"]/div/p[1]/strong//text()')
        if author_list == "":
            author_list = html.xpath('//div[@class="row"]/div/strong//text()')
        for i in author_list:
            if "and" in i:
                try:
                    index = author_list.index(i)
                except ValueError:
                    pass
                else:
                    author_list = author_list[:index+2]
                    break
        for author in author_list:
            if "Figure" in author:
                index_f = author_list.index(author)
                author_list.pop(index_f)
                continue
        author = ",".join(author_list)
        # match position
        position_list = html.xpath('//div[@class="row"]/div[@class="col-md-9 full-text"]/p[position()>1]//text()')
        for i in position_list:
            if (i == "Received Date:") or (i == "Received date:") or (i == "Received date: "):
                try:
                    index_p = position_list.index(i)
                except ValueError:
                    pass
                else:
                    position_list = position_list[:index_p]
                    break
        position = ",".join(position_list)
        # match email (AJAX load)
        try:
            email = html.xpath('//dd//text()[last()]')[-1].strip(" ")
        except IndexError:
            email = "NA"
            ls = [title, author, position, email]
            print(ls)
            print("start saving")
            # save_info2_csv(ls)
        else:
            # dict save
            ls = [title, author, position, email]
            print(ls)
            print("start saving")
            # save_info2_csv(ls)

def get_page_title_href_list():
    """this function:get title url of show_page"""
    # random choice User-Agent
    headers = random.choice(user_agent_list)
    # random choice proxy
    socks5_proxy = '101.251.200.133:45990'
    proxies = {
        'http': 'socks5://' + socks5_proxy,
        'https': 'socks5://' + socks5_proxy
    }
    url = "https://www.omicsonline.org/archive/jpb-volume-9-issue-8-year-2016.html"
    time.sleep(random.randint(1, 2))
    try:
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=30)
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
        # use 're' model match title href
        pattern_title_href = re.compile('<strong>.*?<a href="(.*?)"')
        title_href_list = re.findall(pattern_title_href, page_html)[1:-1]
        print(title_href_list)
        return title_href_list



if __name__ == "__main__":
    # callback User-Agent
    user_agent_list = get_user_agent()
    # create instance for class
    proxy_obj = ProxyPool()
    proxy_list = proxy_obj.get_kuai()
    get_one_page('https://www.omicsonline.org/open-access/response-of-potato-solanum-tuberosum-l-varieties-to-nitrogen-andpotassium-fertilizer-rates-in-central-highlands-of-ethiopia-2329-8863-1000250.php?aid=84179', user_agent_list)