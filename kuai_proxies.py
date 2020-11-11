import requests
from multiprocessing import Process
import os
import time
from datetime import datetime
import random
import re




def write2txt(url_list, file_name):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
	for url in url_list:
		time.sleep(random.choice([0.1, 0.3, 0.5, 0.7, 0.9]))
		try:
			r = requests.get(url, headers=headers)
		except Exception as e:
			print(e)
			continue
		html = r.text
		result_list = re.findall(r'<tr>.*?data-title="IP">(.*?)</td>.*?data-title="PORT">(.*?)</td>.*?data-title="匿名度">(.*?)</td>.*?data-title="类型">(.*?)</td>.*?data-title="位置">(.*?)</td>.*?data-title="响应速度">(.*?)</td>.*?data-title="最后验证时间">(.*?)</td>', html, re.S)
		if result_list:
			with open(file_name, 'a', encoding='utf8') as fw:
				for i in result_list:
					line = 'ip:' + i[0] + ',' + 'port:' + i[1] + ',' + '匿名度:' + i[2] + ',' + '类型:' + i[3] + ',' + '位置:' + i[4] + ',' + '响应速度:' + i[-2] + ',' + '最后验证时间:' + i[-1] + '\n'
					fw.write(line)





if __name__ == "__main__":
	begin_time = datetime.now()
	basic_path = r'C:\Users\mi\Desktop\proxies'
	file_1 = os.path.join(basic_path, 'proxies1.txt')
	file_2 = os.path.join(basic_path, 'proxies2.txt')
	file_3 = os.path.join(basic_path, 'proxies3.txt')
	file_4 = os.path.join(basic_path, 'proxies4.txt')
	basic_url = 'https://www.kuaidaili.com/free/inha/'
	url_list1 = [basic_url + str(i) for i in range(1, 1000)]
	url_list2 = [basic_url + str(i) for i in range(1000, 2000)]
	url_list3 = [basic_url + str(i) for i in range(2000, 3000)]
	url_list4 = [basic_url + str(i) for i in range(3000, 3726)]
	p1 = Process(target=write2txt, args=(url_list1, file_1))
	p2 = Process(target=write2txt, args=(url_list2, file_2))
	p3 = Process(target=write2txt, args=(url_list3, file_3))
	p4 = Process(target=write2txt, args=(url_list4, file_4))
	p1.start()
	p2.start()
	p3.start()
	p4.start()
	p1.join()
	p2.join()
	p3.join()
	p4.join()
	end_time = datetime.now()
	print("任务开始时间: %s, 结束时间: %s" % (begin_time, end_time))
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
# r = requests.get('https://www.kuaidaili.com/free/inha/1')
# html = r.text
# result_list = re.findall(r'<tr>.*?data-title="IP">(.*?)</td>.*?data-title="PORT">(.*?)</td>.*?data-title="匿名度">(.*?)</td>.*?data-title="类型">(.*?)</td>.*?data-title="位置">(.*?)</td>.*?data-title="响应速度">(.*?)</td>.*?data-title="最后验证时间">(.*?)</td>', html, re.S)
# # print(result_list)
# # print(len(result_list))
# with open(r'C:\Users\mi\Desktop\proxies\proxies.txt', 'a', encoding='utf8') as fw:
# 	for i in result_list:
# 		line = 'ip:' + i[0] + ',' + 'port:' + i[1] + ',' + '匿名度:' + i[2] + ',' + '类型:' + i[3] + ',' + '位置:' + i[4] + ',' + '响应速度:' + i[-2] + ',' + '最后验证时间:' + i[-1] + '\n'
# 		fw.write(line)