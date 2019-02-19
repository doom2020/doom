"""此模块用来创建代理池"""
import re
import requests
import time
import random

class ProxyPool:
    def __init__(self, timeout_retry_count=3, code_abnormal_retry_count=3):
        self.timeout_retry_count = timeout_retry_count
        self.code_abnormal_retry_count = code_abnormal_retry_count
        self.check_proxy_url = "https://www.baidu.com/"
        self.wuyou_url = "http://www.data5u.com/"
        self.xici_url = "https://www.xicidaili.com/nn/1"
        self.kuai_url = "https://www.kuaidaili.com/free/"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        self.proxy_list = []

    def timeout_dealwith(self, function):
        """页面请求超时处理"""
        print("页面请求超时")
        self.timeout_retry_count -= 1
        if self.timeout_retry_count < 0:
            return None
        else:
            return function
    def code_abnormal_dealwith(self, function):
        """请求code异常处理"""
        print("请求code异常")
        self.code_abnormal_retry_count -= 1
        if self.code_abnormal_retry_count < 0:
            return None
        else:
            return function
    def check_proxy_vaild(self, proxy):
        """判断获取的proxy是否可用"""
        try:
            resp = requests.get(self.check_proxy_url, headers=self.headers, proxies=proxy, timeout=None)
        except:
            print("此{}连接异常".format(proxy))
        else:
            time.sleep(random.randint(1, 2))
            code = resp.status_code
            if code == 200:
                self.proxy_list.append(proxy)
            else:
                print("代理{}是无效的".format(proxy))
            print("列表内共有{}个代理可用".format(len(self.proxy_list)))


    def get_wuyou(self):
        try:
            resp = requests.get(self.wuyou_url, headers=self.headers, timeout=None)
        except TimeoutError:
            time.sleep(random.randint(1, 2))
            self.timeout_dealwith(self.get_wuyou())
        else:
            code = resp.status_code
            if code != 200:
                time.sleep(random.randint(1, 2))
                self.code_abnormal_dealwith(self.get_wuyou())
            else:
                resp.encoding = "utf-8"
                page_html = resp.text
                pattern = re.compile('<ul class="l2">.*?<li>(.*?)</li>.*?<li.*?>(.*?)</li>.*?<li>(.*?)</li>.*?<li>(.*?)</li>.*?</ul>', re.S)
                result_list = re.findall(pattern, page_html)
                print(result_list)
                for result in result_list:
                    if result[2] == "高匿":
                        proxy = {
                            result[-1]: result[0]+":"+result[1]
                        }
                        print(proxy)
                        self.check_proxy_vaild(proxy)
                    else:
                        continue

    def get_xici(self):
        try:
            resp = requests.get(self.xici_url, headers=self.headers, timeout=None)
        except TimeoutError:
            time.sleep(random.randint(1, 2))
            self.timeout_dealwith(self.get_xici())
        else:
            code = resp.status_code
            if code != 200:
                time.sleep(random.randint(1, 2))
                self.code_abnormal_dealwith(self.get_xici())
            else:
                resp.encoding = "utf-8"
                page_html = resp.text
                pattern = re.compile('<tr class="odd">.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td class="country".*?<td>(.*?)</td>.*?</tr>', re.S)
                result_list = re.findall(pattern, page_html)
                print(result_list)
                for result in result_list:
                    proxy = {
                        result[-1]: result[0]+":"+result[1]
                    }
                    print(proxy)
                    self.check_proxy_vaild(proxy)

    def get_kuai(self):
        try:
            resp = requests.get(self.kuai_url, headers=self.headers, timeout=None)
        except TimeoutError:
            time.sleep(random.randint(1, 2))
            self.timeout_dealwith(self.get_kuai())
        else:
            code = resp.status_code
            if code != 200:
                time.sleep(random.randint(1, 2))
                self.code_abnormal_dealwith(self.get_kuai())
            else:
                resp.encoding = "utf-8"
                page_html = resp.text
                pattern = re.compile(
                    '<tr>.*?<td data-title="IP">(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td data-title="类型">(.*?)</td>.*?</tr>',
                    re.S)
                result_list = re.findall(pattern, page_html)
                print(result_list)
                for result in result_list:
                    proxy = {
                        result[-1]: result[0] + ":" + result[1]
                    }
                    print(proxy)
                    self.check_proxy_vaild(proxy)

if __name__ == "__main__":
    proxy_obj = ProxyPool()
    proxy_obj.get_wuyou()
    proxy_obj.get_xici()
    proxy_obj.get_kuai()
