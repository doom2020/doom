"""
灰度图片噪点去除
采用9宫格比对,当前点与周围8点
BBB
BAB
BBB
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# 获取灰度图像
im_read = cv.imread(r'C:\Users\mi\Desktop\code.jpg', cv.IMREAD_GRAYSCALE)
# 二值化处理
img = np.where(im_read >100, 255, 0)
# 获取图片高宽(行，列)
height,width = img.shape
i,j = (0,0)
cur_pixel = img[i,j]
white_pixel = 255
for i in range(height):
	for j in range(width):
		if i == 0:
			if j == 0:
				# 左上角4个点
				sum_pixel = int(cur_pixel) + int(img[i, j+1]) + int(img[i+1, j] + int(img[i+1, j+1]))
				if sum_pixel >= 2 * white_pixel:
					img[i, j] = white_pixel
			elif j == width-1:
				# 右上角4个点
				sum_pixel = int(cur_pixel) + int(img[i, j-1]) + int(img[i+1, j]) + int(img[i+j, j-1])
				if sum_pixel >= 2 * white_pixel:
					img[i,j] = white_pixel
			else:
				# 第一行中间位置6个点
				sum_pixel = int(cur_pixel) + int(img[i, j-1]) + int(img[i+1, j-1]) + int(img[i+1, j]) + int(img[i+1, j+1]) + int(img[i+1, j+1])
				if sum_pixel >= 3 * white_pixel:
					img[i,j] = white_pixel
		elif i == height-1:
			if j == 0:
				# 左下角4个点
				sum_pixel = int(cur_pixel) + int(img[i-1, j]) + int(img[i-1, j+1]) + int(img[i, j+1])
				if sum_pixel >= 2 * white_pixel:
					img[i,j] = white_pixel
			elif j == width-1:
				# 右下角4个点
				sum_pixel = int(cur_pixel) + int(img[i, j-1]) + int(img[i-1, j-1]) + int(img[i-1, j])
				if sum_pixel >= 2 * white_pixel:
					img[i,j] = white_pixel
			else:
				# 最后一行中间位置6个点
				sum_pixel = int(cur_pixel) + int(img[i, j-1]) + int(img[i-1, j-1]) + int(img[i-1, j]) + int(img[i-1, j+1]) + int(img[i, j+1])
				if sum_pixel >= 3 * white_pixel:
					img[i,j] = white_pixel
		else:
			if j == 0:
				# 中间行第一列6点
				sum_pixel = int(cur_pixel) + int(img[i-1, j]) + int(img[i-1, j+1]) + int(img[i, j+1]) + int(img[i+1, j+1]) + int(img[i+1, j])
				if sum_pixel >= 3 * white_pixel:
					img[i,j] = white_pixel
			elif j == width-1:
				# 中间行最后一列6点
				sum_pixel = int(cur_pixel) + int(img[i-1, j]) + int(img[i-1, j-1]) + int(img[i, j-1]) + int(img[i+1, j-1]) + int(img[i+1, j])
				if sum_pixel >= 3 * white_pixel:
					img[i,j] = white_pixel
			else:
				# 中间行中间列9点
				sum_pixel = int(cur_pixel) + int(img[i-1, j]) + int(img[i-1, j+1]) + int(img[i, j+1]) + int(img[i+1, j+1]) + int(img[i+1, j]) + int(img[i+1, j-1]) + int(img[i, j-1]) + int(img[i-1, j-1])
				if sum_pixel >= 7 * white_pixel:
					img[i,j] = white_pixel

plt.subplot(231),plt.imshow(img,'gray'),plt.title('ORIGINAL')
plt.show()