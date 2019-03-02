"""
Author:doom
datetime:2019.2.28
email:408575225@qq.com
github:doom2020
function:setting the proxy and User-Agent
comment:if you update my code,please update the comment as too,thanks

"""

import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def test_requests_socks5_proxy():
    """this function:setting proxy for requests use socks5"""
    socks5_proxy = '101.251.200.133:8888'
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

def test_selenium_phantomjs_socks5_proxy():
    """this function:setting phantomjs socks5 proxy and User-Agent"""
    test_url = 'http://httpbin.org/get'
    # setting User-Agent
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11")
    # setting not load image(False)
    dcap["phantomjs.page.settings.loadImages"] = False
    # setting socks5 proxy
    service_args = [
        '--proxy=101.251.200.133:8888',
        '--proxy-type=socks5'
    ]
    # setting http proxy
    # service_args = [
    #     '--proxy=10.128.196:8080',
    #     '--proxy-type=http'
    # ]
    # setting https proxy
    # service_args = [
    #     '--proxy=10.128.196:8080',
    #     '--proxy-type=https'
    # ]
    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    driver.get(test_url)
    print(driver.page_source)

def test_selenium_chrome_socks5_proxy():
    """this function:setting chrome socks5 proxy and User-Agent"""
    test_url = 'http://httpbin.org/get'
    socks5_proxy = '101.251.200.133:8888'
    # setting chrome request settings
    chromeOptions = webdriver.ChromeOptions()
    # setting socks5 proxy
    proxy = "--proxy-server=socks5://" + socks5_proxy
    # setting User-Agent
    user_agent = "user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    # setting http proxy
    # proxy = "--proxy-server=http://" + socks5_proxy
    # setting https proxy
    # proxy = "--proxy-server=https://" + socks5_proxy
    chromeOptions.add_argument(proxy)
    chromeOptions.add_argument(user_agent)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.get(test_url)
    print(driver.page_source)


if __name__ == "__main__":
    test_requests_socks5_proxy()
    test_selenium_chrome_socks5_proxy()
    test_selenium_phantomjs_socks5_proxy()