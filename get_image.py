"""
制作单个验证码带标注500张
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

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
	file_path = r'C:\Users\mi\Desktop\code_img'
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

if __name__ == '__main__':
	for i in range(1, 501):
		get_image(i)
		print("第: %s张完成" % i)