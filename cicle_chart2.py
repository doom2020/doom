"""
快代理代理ip省份top10饼图分布
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
n_count = 0
with open(file, 'r', encoding='utf8') as fr:
	while True:
		line = fr.readline()
		if not line:
			break
		info = line.split(',')[-3]
		if "省" in info:
			aa = info.split(':')[-1].split(' ')
			for j in aa:
				if "省" in j:
					bb = j
					break
			index = bb.index("省")
			# print(index)
			# print(info)
			content = bb[: index+1]
			if content in labels:
				for i in label_count:
					if i['label'] == content:
						i['count'] += 1
						break
			else:
				labels.append(content)
				dic = {"label": content, 'count': 1}
				label_count.append(dic)
		else:
			others = '未知'
			n_count += 1

label_count.append({"label": others, 'count': n_count})

# print(labels)
# print(len(labels))
print(label_count)
print(len(label_count))

label_ls = []
sizes = []
count = 0
for i in label_count:
	if i['label'] and i['count'] >= 100 and (i['label'] != '未知'):
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
label_ls = label_ls[:10]
sizes = sizes[:10]
explode = [i*0 for i in range(len(label_ls))]  # only "explode" the 2nd slice (i.e. 'Hogs')
explode[1] = 0.1
explode = explode[:10]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=label_ls, autopct='%.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()