# -*- coding: utf-8 -*-
"""
Author:doom
datetime:2019.2.26
email:408575225@qq.com
github:doom2020
function: use selenium + phantomjs + chrome model get old journal
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
import multiprocessing
import os
import threading


def save_info2_csv(ls, p_lock, t_lock):
    """this function:save data to csv file"""
    print("上进程锁")
    p_lock.acquire()
    print("上线程锁")
    t_lock.acquire()
    with open(r'C:\Users\Administrator\Desktop\2019_3_12_old_begin.csv', 'a', newline="", encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(ls)
    print("解线程锁")
    t_lock.release()
    print("解进程锁")
    p_lock.release()


# use old journal for example: 2017.5.4-2017.5.1 or year < 2018，because the email is JS load,so,use selenium + chrome
def get_one_page(url, summary_title, user_agent_list, p_lock, t_lock):
    """this function:get info from detail page (last child page)"""
    print("当前线程pid:{},ppid:{}".format(os.getpid(), os.getppid()))
    data_count = 0
    try:
        if int(summary_title[-1]) >= 8:
            return
    except Exception as e:
        print(e)
        return
    # # VPN socks5代理ip和端口
    socks5_proxy = '39.96.38.189:45990'
    # 修改selenium请求设置
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--disable-gpu')
    proxy = "--proxy-server=socks5://" + socks5_proxy
    user_agent = "user-agent=" + random.choice(user_agent_list)["User-Agent"]
    chromeOptions.add_argument(proxy)
    chromeOptions.add_argument(user_agent)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.set_page_load_timeout(random.randint(50, 80))
    try:
        driver.get(url)
        print("请求页面成功")
    except Exception as e:
        print(e)
        driver.quit()
        time.sleep(random.randint(1, 2))
        return
    else:
        print("执行js语句开始")
        js1 = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js1)
        js2 = "var q=document.documentElement.scrollTop=350"
        driver.execute_script(js2)
        # js加载完成后获取页面的html
        page_html = driver.page_source
        driver.quit()
        html = etree.HTML(page_html)
        # 匹配标题(标题OK)
        title = ",".join(html.xpath('//h1[@class="fulltext_h1heading margin-t-0"]//text()')).replace("\n", " ")
        print("主题是:", title)
        # 匹配作者()
        author_list = html.xpath('//div[@class="row"]/div/table[1]/tbody/tr[1]/td/strong//text()')
        print("第一次author_list:", author_list)
        print("author_list的布尔值:", bool(author_list))
        if not author_list:
            author_list = html.xpath('//div[@class="row"]/div/p[1]/strong//text()')
            print("第二次author_list:", author_list)
            if not author_list:
                author_list = html.xpath('//div[@class="row"]/div/strong//text()')
                print("第三次author_list:", author_list)
        for i in author_list:
            if "and" in i:
                try:
                    index = author_list.index(i)
                except ValueError:
                    pass
                else:
                    author_list = author_list[:index + 2]
                    break
        for author in author_list:
            if "Figure" in author:
                index_f = author_list.index(author)
                author_list.pop(index_f)
                continue
        author = ",".join(author_list)
        print("第一次author:", author)
        if len(author) >= 500:
            author = "NA"
        print("最终的author", author)
        # match position
        position_list = html.xpath('//div[@class="row"]/div/table[1]/tbody/tr[2]/td/text()')
        print("第一次position_list:", position_list)
        if not position_list:
            position_list = html.xpath('//div[@class="row"]/div[@class="col-md-9 full-text"]/p[position()>1]//text()')
            print("第二次position_list:", position_list)
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
        if len(position) >= 500:
            position = "NA"
        # match email (AJAX load)
        print("最终position", position)
        try:
            email = html.xpath('//table[@class="table"]/tbody/tr[3]/td[2]//text()')[-1].strip(" ")
        except IndexError:
            email = ""
            if email == "":
                try:
                    email = html.xpath('//dd//text()[last()]')[-1].strip(" ")
                except IndexError:
                    email = "NA"
                    ls = [title, author, position, email]
                    print(ls)
                    print("start saving")
                    if "@" not in email or author == "":
                        pass
                    save_info2_csv(ls, p_lock, t_lock)
                # dict save
                ls = [title, author, position, email]
                print(ls)
                print("start saving")
                if "@" not in email or author == "":
                    pass
                save_info2_csv(ls, p_lock, t_lock)
        else:
            ls = [title, author, position, email]
            print(ls)
            print("start saving")
            if "@" not in email or author == "":
                pass
            save_info2_csv(ls, p_lock, t_lock)


def get_page_title_href_list(all_year_journal_href_list, user_agent_list, p_lock):
    """get all url form show_page (third child page)"""
    # random chose User-Agent
    headers = random.choice(user_agent_list)
    # requests setting socks5 proxy
    socks5_proxy = '39.96.38.189:45990'
    proxies = {
        'http': 'socks5://' + socks5_proxy,
        'https': 'socks5://' + socks5_proxy
    }
    for url in all_year_journal_href_list:
        print("第三个子界面url类型：", type(url))
        print("第三个子界面url:", url)
        time.sleep(random.randint(1, 2))
        try:
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        except Exception as e:
            print(e)
            print("url:{}request page fail".format(url))
            time.sleep(random.randint(1, 2))
            continue
        else:
            resp.encoding = "utf-8"
            page_html = resp.text
            pattern_summary_title = re.compile('<title>(.*?)</title>')
            pattern_title_href = re.compile('<strong>.*?<a href="(.*?)"')
            try:
                summary_title = re.findall(pattern_summary_title, page_html)[0]
                title_href_list = re.findall(pattern_title_href, page_html)[1:-1]
            except IndexError:
                continue
            # 使用多线程处理
            print("开始创建多线程")
            for href in title_href_list:
                t_lock = threading.Lock()
                t = threading.Thread(target=get_one_page, args=(href, summary_title, user_agent_list, p_lock, t_lock))
                t.start()
                t.join()
            print("the current process's all threading is over")


def get_all_year_journal_href(valid_classify_url, user_agent_list, p_lock):
    """this function:get all url of current classify journal (second child page)"""
    print("当前进程pid:{},ppid:{}".format(os.getpid(), os.getppid()))
    # init href list
    all_year_journal_href_list = []
    headers = random.choice(user_agent_list)
    try:
        resp = requests.get(valid_classify_url, headers=headers, proxies=None, timeout=30)
    except Exception as e:
        print(e)
        print("url:{}.request page fail".format(valid_classify_url))
        return
    else:
        time.sleep(random.randint(1, 2))
        resp.encoding = "utf-8"
        page_html = resp.text
        # use xpath math
        html = etree.HTML(page_html)
        # get all math url
        all_href_list = html.xpath('//div[@class="card mb-3"]//a/@href')
        for href in all_href_list:
            # delete the url has "php" str
            try:
                if href[-4:] == "html":
                    all_year_journal_href_list.append(href)
            except IndexError:
                continue
    get_page_title_href_list(all_year_journal_href_list, user_agent_list, p_lock)


def get_archive(all_classify_href_list):
    """this function:get has 'archive' element' href (first child page)"""
    valid_classify_list = []
    num = 0
    count = len(all_classify_href_list)
    headers = random.choice(user_agent_list)
    socks5_proxy = '39.96.38.189:45990'
    proxies = {
        'http': 'socks5://' + socks5_proxy,
        'https': 'socks5://' + socks5_proxy
    }
    for classify_url in all_classify_href_list:
        print("第一个子界面url类型：", type(classify_url))
        try:
            resp = requests.get(classify_url, headers=headers, proxies=proxies, timeout=15)
        except Exception as e:
            print(e)
        else:
            resp.encoding = "utf-8"
            page_html = resp.text
            # use 're' model match 'archive' element
            html = etree.HTML(page_html)
            archive = html.xpath('//nav[@class="nav"]/a[3]/@href')
            print("链接:", archive)
            # 这里archive 是 list 类型
            if archive:
                valid_classify_list.append(archive[0])
                print("get url that has archive:", archive[0])
            else:
                print("this url page does not exist archive")
                print("url:{}is invalid".format(classify_url))
            num += 1
            rate = float(num / count) * 100
            print("completed rate:{}%".format(rate))
    print("valid url count:", len(valid_classify_list))
    return valid_classify_list


def get_classify_href_list():
    """this function:get all classify journal url (parent page)"""
    # init the href list
    all_classify_href_list = []
    # setting user-agent
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11")
    # # setting not load image(False)
    # dcap["phantomjs.page.settings.loadImages"] = False
    # driver = webdriver.PhantomJS(desired_capabilities=dcap)
    # driver.set_page_load_timeout(200)
    url = "https://www.omicsonline.org/scientific-journals.php"
    # # VPN socks5代理ip和端口
    socks5_proxy = '39.96.38.189:45990'
    # 修改selenium请求设置
    chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_argument('--headless')
    # chromeOptions.add_argument('--disable-gpu')
    proxy = "--proxy-server=socks5://" + socks5_proxy
    user_agent = "user-agent=" + random.choice(user_agent_list)["User-Agent"]
    chromeOptions.add_argument(proxy)
    chromeOptions.add_argument(user_agent)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.set_page_load_timeout(random.randint(50, 80))
    # headers = random.choice(user_agent_list)
    # resp = requests.get(url, headers=headers)
    # resp.encoding = "utf-8"
    # page_html = resp.text
    # print(page_html)
    try:
        driver.get(url)
    except Exception as e:
        print("requests timeout:", e)
        driver.quit()
        return
    js1 = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js1)
    js2 = "var q=document.documentElement.scrollTop=100"
    driver.execute_script(js2)
    time.sleep(8)
    page_html = driver.page_source
    print(page_html)
    time.sleep(2)
    driver.quit()
    # use 're' model match all classify journal
    pattern_classify = re.compile('<a.*?href="(.*?)".*?</a>', re.S)
    classify_href_list = re.findall(pattern_classify, page_html)
    # print(classify_href_list)
    # delete the"php"href
    for classify_href in classify_href_list:
        # print(classify_href)
        if classify_href[:27] == "https://www.omicsonline.org" and classify_href[-3:] == "php":
            all_classify_href_list.append(classify_href)
    print(all_classify_href_list)
    print("href number:", len(all_classify_href_list))
    return all_classify_href_list


if __name__ == "__main__":
    # callback get_user_agent()
    user_agent_list = get_user_agent()
    # process lock(in order to writer file to csv)
    p_lock = multiprocessing.Lock()
    # callback get_classify_href_list(), get all classify journal href,this is parent page(https://www.omicsonline.org/scientific-journals.php)
    while True:
        time.sleep(random.randint(3, 6))
        all_classify_href_list = get_classify_href_list()
        if len(all_classify_href_list) >= 500:
            break
    print("main process1 over")
    # callback get_archive(), get have 'archive'element url,this is first child page (https://www.omicsonline.org/advances-crop-science-and-technology.php)
    valid_classify_list = get_archive(all_classify_href_list)
    print("main process2 over")
    print("开始创建多进程")
    count = len(valid_classify_list)
    count_begin = 0
    for valid_classify_url in valid_classify_list:
        if count_begin == int(count/2):
            break
        count_begin += 1
        p = multiprocessing.Process(target=get_all_year_journal_href, args=(valid_classify_url, user_agent_list, p_lock))
        p.start()
        p.join()
    print("all process is over")