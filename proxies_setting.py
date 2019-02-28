"""
Author:doom
function:setting the proxy use socks5

"""

import requests
from selenium import webdriver

def test_requests_proxy():
    socks5_proxy = '101.251.200.133:45990'
    proxies = {
        'http': 'socks5://' + socks5_proxy,
        'https': 'socks5://' + socks5_proxy
    }
    test_url = 'http://httpbin.org/get'
    headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
    try:
        resp = requests.get(test_url, headers=headers, proxies=proxies)
        print(resp.text)
    except Exception as e:
        print('error', e)

def test_selenium_proxy():
    test_url = 'http://httpbin.org/get'
    service_args = [
        '--proxy=101.251.200.133:45990',
        '--proxy-type=socks5'
    ]
    driver = webdriver.PhantomJS(service_args=service_args)
    driver.get(test_url)
    print(driver.page_source)


if __name__ == "__main__":
    test_selenium_proxy()