"""
scikit-learn 验证码的识别分类
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
import cv2 as cv
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split

# 原始图片目录
file_path = r'C:\Users\mi\Desktop\code_img'
# 处理后图片目录
filter_path = r'C:\Users\mi\Desktop\code_img_filter'
# 随机大写字母:
def rndChar():
    return chr(random.randint(65, 90))

# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def get_image(i):
	width = 60
	height = 60
	image = Image.new('RGB', (width, height), (255, 255, 255))
	# 创建Font对象:
	font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 36)
	# 创建Draw对象:
	draw = ImageDraw.Draw(image)
	# 填充每个像素:
	for x in range(width):
	    for y in range(height):
	        draw.point((x, y), fill=rndColor())
	# 输出文字:
	text = rndChar()
	print(text)
	draw.text((15, 12), text, font=font, fill=rndColor2())
	# image = image.filter(ImageFilter.BLUR)
	img_name = str(i) + '_' + text + '.jpg'
	file_name = os.path.join(file_path, img_name)
	image.save(file_name, 'jpeg')


def filter_image():
	file_names = os.listdir(file_path)
	print(file_names)
	# images = [os.path.join(file_path, i) for i in file_names]
	for i in file_names:
		image_name = os.path.join(file_path, i)
		# 获取灰度图像
		image_new_name = os.path.join(filter_path, i)
		im_read = cv.imread(image_name, cv.IMREAD_GRAYSCALE)
		# 二值化处理
		img = np.where(im_read >110, 255, 0)
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
		cv.imwrite(image_new_name, img)


def train_model():
	files = os.listdir(filter_path)
	file_names = [os.path.join(filter_path, i) for i in files]
	last_text = [i.split('_')[-1].split('.')[0] for i in file_names[-5:]]
	img_ls = []
	text_ls = []
	for i in file_names:
		im_read = cv.imread(i)
		img_1d_array = im_read.flatten()
		img_ls.append(img_1d_array)
		text = i.split('_')[-1].split('.')[0]
		text_ls.append(text)
		print(i)
	# datas = np.array(img_ls)
	# targets = np.array(text_ls)
	# print(datas)
	# print(targets)
	# print(datas.shape)
	# print(targets.shape)
	clf = svm.SVC(gamma=0.001)
	clf.fit(img_ls[:-1], text_ls[:-1])
	result = clf.predict(img_ls[-1:])
	print(last_text)
	print(result)


if __name__ == '__main__':
	train_model()