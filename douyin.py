import requests
from selenium import webdriver
import random
import time


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"}



# req = requests.get('https://v26-web.douyinvod.com/26ce8d9a05bdbba2720fc8a434983d9e/60fbf1f4/video/tos/cn/tos-cn-ve-15/9e395e7c9f0241f4b421f083f3efe46b/?a=6383&br=1491&bt=1491&cd=0%7C0%7C0&ch=26&cr=0&cs=0&cv=1&dr=0&ds=3&er=&ft=0J.120FFckag3&l=021627120428386fdbddc0100fff0030ad112d4000000915a765d&lr=all&mime_type=video_mp4&net=0&pl=0&qs=0&rc=MztkNzg6ZnJzNTMzNGkzM0ApNjkzMzRlNmQ3NzM1OTM6N2deY2VkcjRnLWVgLS1kLTBzc2FgYjJhLTExNGIyYC4tM146Yw%3D%3D&vl=&vr=', headers=headers)
# print(req.status_code)
# with open("aaa.mp4", 'wb') as fw:
#     for chuck in req.iter_content(chunk_size=4096):
#         print(chuck)
#         fw.write(chuck)

# print(req.status_code)


def loading_page():
    chrome_option = webdriver.ChromeOptions()
    # chrome_option.add_argument('--headless')
    # chrome_option.add_argument('--disable-gpu')
    proxy = "--proxy-server=http://" + '218.2.214.107:80'
    user_agent = "user-agent=" + headers['user-agent']
    # accept = "accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    # accept_encoding = "accept-encoding=gzip, deflate, br"
    # accept_language = "accept-language=zh-CN,zh;q=0.9,en;q=0.8"
    # sec_ch_ua = 'sec-ch-ua=" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"'
    # sec_ch_ua_mobile = "sec-ch-ua-mobile=?0"
    # sec_fetch_dest = "sec-fetch-dest=document"
    # sec_fetch_mode = "sec-fetch-mode=navigate"
    # sec_fetch_site = "sec-fetch-site=none"
    # sec_fetch_user = "sec-fetch-user=?1"
    # upgrade_insecure_requests = "upgrade-insecure-requests=1"
    chrome_option.add_argument(proxy)
    chrome_option.add_argument(user_agent)
    # chrome_option.add_argument(accept)
    # chrome_option.add_argument(accept_encoding)
    # chrome_option.add_argument(accept_language)
    # chrome_option.add_argument(sec_ch_ua)
    # chrome_option.add_argument(sec_ch_ua_mobile)
    # chrome_option.add_argument(sec_fetch_dest)
    # chrome_option.add_argument(sec_fetch_mode)
    # chrome_option.add_argument(sec_fetch_site)
    # chrome_option.add_argument(sec_fetch_user)
    # chrome_option.add_argument(upgrade_insecure_requests)
    driver = webdriver.Chrome(chrome_options=chrome_option)
    driver.set_page_load_timeout(random.randint(50, 80))
    url = 'https://www.douyin.com/channel/300204'
    try:
        driver.get(url)
    except Exception as e:
        print("requests timeout:", e)
        driver.quit()
        return False
    time.sleep(10)
    driver.refresh()
    video_count = 0
    while True:
        if video_count >= 50:
            break
        js1 = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js1)
        video_count += 1
        time.sleep(3)
    driver.quit()




if __name__ == "__main__":
    loading_page()

