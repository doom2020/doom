"""
Author:doom
datetime:2019.2.28
email:408575225@qq.com
github:doom2020
function:get proxy pool
comment:if you update my code,please update the comment as too,thanks

"""
import re
import requests
import time
import random
# from mysql_power import MysqlHelper
# from mongo_power import MyMongo

class ProxyPool:
    """this class is create proxy pool"""
    def __init__(self, timeout_retry_count=3, code_abnormal_retry_count=3, request_timeout=15, normal_code=200):
        self.timeout_retry_count = timeout_retry_count
        self.code_abnormal_retry_count = code_abnormal_retry_count
        self.timeout = request_timeout
        self.normal_code = normal_code
        self.check_proxy_url = "https://www.baidu.com/"
        self.xici_url = "https://www.xicidaili.com/nn/"
        self.kuai_url = "https://www.kuaidaili.com/free/"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        self.proxy_list = []

    def timeout_dealwith(self, callback):
        """this method :deal with the page request timeout exception"""
        print("the page request timeout")
        self.timeout_retry_count -= 1
        if self.timeout_retry_count < 0:
            return None
        else:
            return callback
    def code_abnormal_dealwith(self, callback):
        """this method:deal with the page request code abnormal(is not 200)"""
        print("request code abnormal")
        self.code_abnormal_retry_count -= 1
        if self.code_abnormal_retry_count < 0:
            return None
        else:
            return callback
    def check_proxy_vaild(self, proxy):
        """this method:check the proxy is valid?,that we got from web"""
        try:
            resp = requests.get(self.check_proxy_url, headers=self.headers, proxies=proxy, timeout=self.timeout)
        except:
            print("the{}connect abnormal".format(proxy))
        else:
            time.sleep(random.randint(1, 2))
            code = resp.status_code
            if code == self.normal_code:
                self.proxy_list.append(proxy)
            else:
                print("proxy{}is not valid".format(proxy))
            print("the list have{}proxy is valid".format(len(self.proxy_list)))

    def get_xici(self):
        """this method:get proxy from xici web(every page has 40 proxies,I got the five pages)"""
        # if you want to get more and more proxy,please update the'end_page'number
        begin_page = 1
        end_page = 6
        for page in range(begin_page, end_page):
            url = self.xici_url + str(page)
            try:
                resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            except TimeoutError:
                time.sleep(random.randint(1, 2))
                self.timeout_dealwith(self.get_xici())
            else:
                code = resp.status_code
                if code != self.normal_code:
                    time.sleep(random.randint(1, 2))
                    self.code_abnormal_dealwith(self.get_xici())
                else:
                    resp.encoding = "utf-8"
                    page_html = resp.text
                    pattern = re.compile('<tr class="odd">.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td class="country".*?<td>(.*?)</td>.*?</tr>', re.S)
                    result_list = re.findall(pattern, page_html)
                    print(result_list)
                    for result in result_list:
                        # I just want get proxy that the type is 'HTTP',if you want get all,please disabled the code
                        if result[-1] == "HTTPS":
                            continue
                        proxy = {
                            result[-1]: result[0]+":"+result[1]
                        }
                        print(proxy)
                        self.check_proxy_vaild(proxy)
        return self.proxy_list

    def get_kuai(self):
        """this method:get proxy from kuai web(this web has 15 free proxy)"""
        try:
            resp = requests.get(self.kuai_url, headers=self.headers, timeout=self.timeout)
        except TimeoutError:
            time.sleep(random.randint(1, 2))
            self.timeout_dealwith(self.get_kuai())
        else:
            code = resp.status_code
            if code != self.normal_code:
                time.sleep(random.randint(1, 2))
                self.code_abnormal_dealwith(self.get_kuai())
            else:
                resp.encoding = "utf-8"
                page_html = resp.text
                pattern = re.compile('<tr>.*?<td data-title="IP">(.*?)</td>.*?<td.*?>(.*?)</td>.*?<td data-title="类型">(.*?)</td>.*?</tr>', re.S)
                result_list = re.findall(pattern, page_html)
                print(result_list)
                for result in result_list:
                    # I just want get proxy that the type is 'HTTP',if you want get all,please disabled the code
                    if result[-1] == "HTTPS":
                        continue
                    proxy = {
                        result[-1]: result[0] + ":" + result[1]
                    }
                    print(proxy)
                    self.check_proxy_vaild(proxy)
        return self.proxy_list

    def save_proxy2sql(self):
        """this method:put proxy into mysql database"""
        pass

    def save_proxy2mongo(self):
        """this method:put proxy into mongodb database"""
        pass

    def save_proxy2redis(self):
        """this method:put proxy into redis database"""
        pass


if __name__ == "__main__":
    # create instance for class
    proxy_obj = ProxyPool()
    proxy = proxy_obj.get_kuai()


