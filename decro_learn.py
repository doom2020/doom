import functools
"""
flask自己写的装饰器必须要functiools.wraps，要不然所有被装饰的视图函数的函数名都将是wrap
"""

def log(text):
	def decro(func):
		@functools.wraps(func)
		def wrap(*args, **kwargs):
			print(f'text: {text}, func: {func.__name__}')
			return func(*args, **kwargs)
		return wrap
	return decro



@log('1111')
def test():
	print("hello world")


if __name__ == "__main__":
	test()
	print(test.__name__) # 未加@functools.wraps(func)原来的函数名会被修改(即test函数名改为了wrap)有些依赖函数签名的代码执行就会出错