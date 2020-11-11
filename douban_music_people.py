import requests
from multiprocessing import Process
from multiprocessing import Queue
import re
import random
import os
import time
from datetime import datetime

basic_url = 'https://music.douban.com/artists/genre_page/6/'
img_path = r'C:\Users\mi\Desktop\request\douban_music_people'


def get_page_url(q1, q2):
	page_num = 374
	page_urls = [basic_url + str(i) for i in range(1, page_num + 1)]
	for i in page_urls:
		q1.put(i)

def dealwith_page_url(q1, q2):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
	proxies = {"http": "171.35.170.158:9999"}
	while True:
		page_url = q1.get()
		if not page_url:
			break
		time.sleep(random.choice([0.1, 0.2, 0.3]))
		try:
			r = requests.get(page_url, headers=headers, proxies=proxies)
		except Exception as e:
			print('出错的page_url: %s, 原因: %s' % (page_url, e))
			continue
		html = r.text
		result_ls = re.findall(r'<a class="artist_photo".*?src="(.*?)">', html, re.S)
		for i in result_ls:
			img_url = i.split('"')[0]
			q2.put(img_url)

def get_img_url_and_save(q1, q2):
	img_count = 0
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
	proxies = {"http": "123.54.45.55:9999"}
	while True:
		img_url = q2.get()
		if not img_url:
			break
		time.sleep(random.choice([0.1, 0.2, 0.3]))
		try:
			r = requests.get(img_url, headers=headers, proxies=proxies)
		except Exception as e:
			print("出错的img_url: %s, 原因: %s" % (img_url, e))
			continue
		content = r.content
		img_name = img_url.split('/')[-1]
		img_file = os.path.join(img_path, img_name)
		with open(img_file, 'wb') as fw:
			fw.write(content)
		img_count += 1
		print('第%s张图片下载完成' % img_count)



if __name__ == "__main__":
	begin_time = datetime.now()
	q1 = Queue()
	q2 = Queue()
	p1 = Process(target=get_page_url, args=(q1, q2))
	p2 = Process(target=dealwith_page_url, args=(q1, q2))
	p3 = Process(target=get_img_url_and_save, args=(q1, q2))
	p1.start()
	p2.start()
	p3.start()
	p1.join()
	p2.join()
	p3.join()
	end_time = datetime.now()
	print("任务开始时间: %s, 结束时间: %s" % (begin_time, end_time))
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
# proxies = {"http": "123.55.101.60:9999"}
# url = 'https://music.douban.com/artists/genre_page/6/1'
# r = requests.get(url, headers=headers, proxies=proxies)
# html = r.text
# result_ls = re.findall(r'<a class="artist_photo".*?src="(.*?)">', html, re.S)
# img_url_ls = [ i.split('"')[0] for i in result_ls]
# # print(result_ls)
# # print(len(result_ls))
# print(img_url_ls)
# print(len(img_url_ls))

# url2 = 'https://img1.doubanio.com/view/site/median/public/fc00cb95a9b74d9.jpg'

# r2 = requests.get(url2, headers=headers, proxies=proxies)
# content = r2.content
# with open(r'C:\Users\mi\Desktop\ggg.jpg', 'wb') as fw:
# 	fw.write(content)



