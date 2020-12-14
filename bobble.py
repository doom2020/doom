
import random

list_1 = [i for i in range(50)]
random.shuffle(list_1)


# 遍历的趟数为列表的长度减1
# 遍历的趟数(从0开始)为列表的长度减1(最后一趟不用遍历了因为倒数第二趟就排好了)
# 优化冒泡排序(只要有一趟没有发生位置交换说明已经排好了不用再遍历了)
# 每一趟的列表索引值变化(第0趟索引0~7,第一趟0~6,第二趟0~5)比较的后面那个索引都要加1所以要减1
def bubble(ls):
	for i in range(len(ls)-1):
		has_change = False
		for index in range(len(ls)-1-i):
			if ls[index] > ls[index+1]:
				has_change = True
				ls[index], ls[index+1] = ls[index+1], ls[index]
		if not has_change:
			break

		print(ls)


if __name__ == "__main__":
	bubble(list_1)





