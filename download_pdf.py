"""
Author:doom
datetime:2019.3.4
email:408575225@qq.com
github:doom2020
comment:if you update my code,please update my comment,thanks

"""

import requests
import time
import random
from lxml import etree
import os
from get_user_agent import get_user_agent


class DownloadFilePDF:
    def __init__(self):
        self.save_pdf_file_path = r'C:\Users\Administrator\Desktop\pdf_download'
        self.first_page_url = r'http://ijasos.ocerintjournals.org/'
        self.user_agent_list = get_user_agent()

    def download_pdf(self):
        summary_time = 0
        # pdf 文件数量以及命名
        count = 0
        pdf_url_list = self.get_pdf_src()
        for pdf_url in pdf_url_list:
            time_begin = time.time()
            headers = random.choice(self.user_agent_list)
            socks5_proxy = '101.251.200.133:45990'
            proxies = {
                'http': 'socks5://' + socks5_proxy,
                'https': 'socks5://' + socks5_proxy
            }
            try:
                resp = requests.get(pdf_url, headers=headers, proxies=proxies, timeout=30)
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
            resp.encoding = 'utf-8'
            page_html_b = resp.content
            count += 1
            file_name = str(count)+".pdf"
            pdf_file_name = os.path.join(self.save_pdf_file_path, file_name)
            with open(pdf_file_name, 'wb') as pdf_file:
                pdf_file.write(page_html_b)
            time_end = time.time()
            use_time = time_end - time_begin
            summary_time += use_time
            print("第{}个pdf文件下载完毕,花费时间{}秒".format(count, use_time))
        print("下载了{}个pdf文件，总共用的时间{}秒，平均时间{}秒".format(count, summary_time, float(summary_time/count)))


    def get_pdf_src(self):
        pdf_url_list = []
        journal_url_list = self.get_page_url()
        for journal_url in journal_url_list:
            headers = random.choice(self.user_agent_list)
            socks5_proxy = '101.251.200.133:45990'
            proxies = {
                'http': 'socks5://' + socks5_proxy,
                'https': 'socks5://' + socks5_proxy
            }
            try:
                resp = requests.get(journal_url, headers=headers, proxies=proxies, timeout=30)
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
            resp.encoding = 'utf-8'
            page_html = resp.text
            html = etree.HTML(page_html)
            all_href_list = html.xpath('//ul[@class="list-group"]/li/div/a/@href')
            # print(all_href_list)
            'http://ijasos.ocerintjournals.org/download/article-file/615108'
            print("数量:", len(all_href_list))
            for href in all_href_list[1:]:
                url = self.first_page_url + href[1:]
                print(url)
                pdf_url_list.append(url)
        return pdf_url_list



    def get_page_url(self):
        """主页面"""
        journal_url_list = []
        headers = random.choice(self.user_agent_list)
        socks5_proxy = '101.251.200.133:45990'
        proxies = {
            'http': 'socks5://' + socks5_proxy,
            'https': 'socks5://' + socks5_proxy
        }
        try:
            resp = requests.get(self.first_page_url, headers=headers, proxies=proxies, timeout=30)
        except Exception as e:
            print(e)
            return
        resp.encoding = 'utf-8'
        page_html = resp.text
        html = etree.HTML(page_html)
        '/html/body/div[5]/div/div/div[4]/div[2]/div[1]/div/div[2]/div[2]/a'
        '/html/body/div[5]/div/div/div[4]/div[2]/div[1]/div/div[2]/div[3]'
        '/html/body/div[5]/div/div/div[4]/div[2]/div[1]/div/div[2]/div[4]'
        '/html/body/div[5]/div/div/div[4]/div[2]/div[1]/div/div[2]/div[6]'
        journal_href_list = html.xpath('/html/body/div[5]/div/div/div[4]/div[2]/div[1]/div/div[2]//div/a/@href')
        for journal_href in journal_href_list:
            href = journal_href.replace(r'//dergipark.gov.tr/ijasos/', '')
            # print(href)
            url = self.first_page_url + href
            journal_url_list.append(url)
            # print(url)
        return journal_url_list


if __name__ == "__main__":
    download = DownloadFilePDF()
    # download.get_page_url()
    # download.get_pdf_src()
    download.download_pdf()
