import requests
import re
import time
import os
from multiprocessing import Pool
from datetime import datetime
import threading

basic_url = 'https://bing.ioliu.cn/ranking?p='
img_local_path = r'C:\Users\biying_small'

# proxies1 = {"http": "180.118.128.196:9999"}
# proxies2 = {"http": "175.44.109.114:9999"}

def get_imag(page):
	url = basic_url + str(page)
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
	try:
		r = requests.get(url, headers=headers)
	except Exception as e:
		print(e)
		print(url)
		return
	html = r.text
	goods_ls = re.findall(r'<a class="ctrl download" href="(.*?)"', html, re.S)
	print(goods_ls)
	print(len(goods_ls))
	for img_url in goods_ls:
		try:
			img_url = 'https://bing.ioliu.cn' + img_url
			r = requests.get(img_url, headers=headers)
			content = r.content
			file_name = os.path.join(img_local_path, img_url.split('/')[-1].split('?')[0] + '.jpg')
			with open(file_name, 'wb') as fw:
				fw.write(content)
		except Exception as e:
			print(e)
			print(img_url)
			continue

if __name__ == "__main__":
	start_time = datetime.now()
	for i in range(1, 143):
		try:
			t = threading.Thread(target=get_imag, args=(i, ))
		except Exception as e:
			print(e)
			continue
		t.start()
		# t.join()
	end_time = datetime.now()
	print("任务开始时间: %s, 结束时间: %s" %  (start_time, end_time))


# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
# # re_ls = re.findall(r'<div class="mes".*?<a href="(.*?)">.*?</div>', html, re.S)[1:]
# # print(re_ls)
# # 'https://music.douban.com/artists/genre_page/6/2'

# tv_urls = ['https://bing.ioliu.cn/ranking?p=' + str(i) for i in range(1, 142)]

# img_local_path = r'C:\Users\mi\Desktop\request\biying_small'

# # goods_img_ls = []
# 'https://bing.ioliu.cn/photo/MinnewankaBoathouse_ZH-CN0548323518?force=ranking_7'

# # count = 0
# for url in tv_urls:
# 	time.sleep(0.1)
# 	r = requests.get(url, headers=headers)
# 	html = r.text
# 	# print(html)
# 	goods_ls = re.findall(r'<a class="ctrl download" href="(.*?)"', html, re.S)
# 	print(goods_ls)
# 	print(len(goods_ls))
# 	print('第一页请求获取img url 完成')
# # 	goods_img_ls.extend(goods_ls)
# 	for img_url in goods_ls:
# 		# count += 1
# 		img_url = 'https://bing.ioliu.cn' + img_url
# 		print(img_url)
# 		time.sleep(0.1)
# 		r = requests.get(img_url, headers=headers)
# 		print(r.status_code)
# 		content = r.content
# 		file_name = os.path.join(img_local_path, img_url.split('/')[-1].split('?')[0] + '.jpg')
# 		with open(file_name, 'wb') as fw:
# 			fw.write(content)
# 	break
		# print('第: %s张图片下载完成' % count)

# print(goods_img_ls)
# print(len(goods_img_ls))

# for img_url in goods_img_ls:
# 	time.sleep(1)
# 	r = requests.get(img_url, headers=headers)
# 	content = r.content
# 	file_name = os.path.join(img_local_path, img_url.split('/')[-1].split('.')[0] + '.png')
# 	with open(file_name, 'wb') as fw:
# 		fw.write(content)




