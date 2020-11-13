"""
快代理代理ip运营商饼图分布
"""


import matplotlib.pyplot as plt
import os
# Pie chart, where the slices will be ordered and plotted counter-clockwise:

plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

basic_path = r'C:\Users\mi\Desktop\proxies'
file = os.path.join(basic_path, 'proxies.txt')
labels = []
label_count = []
with open(file, 'r', encoding='utf8') as fr:
	while True:
		line = fr.readline()
		if not line:
			break
		info = line.split(',')[-3].split(' ')[-1]
		if info in labels:
			for i in label_count:
				if i['label'] == info:
					i['count'] += 1
					break
		else:
			labels.append(info)
			dic = {"label": info, 'count': 1}
			label_count.append(dic)
print(labels)
print(len(labels))
print(label_count)
print(len(label_count))

label_ls = []
sizes = []
count = 0
for i in label_count:
	if i['label'] and i['count'] >= 1000:
		label_ls.append(i['label'])
		sizes.append(i['count'])
	else:
		if '其他' in label_ls:
			count += i['count']
		else:
			label_ls.insert(0, '其他')
			count += i['count']

sizes.insert(0, count)
# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# sizes = [15, 30, 45, 10]
# print(len(label_ls))
# print(len(sizes))
explode = [i*0 for i in range(len(label_ls))]  # only "explode" the 2nd slice (i.e. 'Hogs')
explode[1] = 0.1

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=label_ls, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()