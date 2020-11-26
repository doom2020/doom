"""
此模块用来测试一下不同的实例是否可以调用缓存数据 测试结果：不能， 使用全局引入可以实现(但不好)

拓展一下：使用单列模式(当整个应用程序只需要一个实例)
"""
from cacheout import LFUCache

"""******不同实例测试以及全局引入测试*********"""
# def get():
# 	global cache1
# 	value = cache1.get_value(1)
# 	print(value)



# class LFUCacheManage:
# 	def __init__(self, maxsize=None, ttl=None, timer=None, default=None):
# 		self.maxsize = maxsize
# 		self.ttl = ttl
# 		self.timer = timer
# 		self.default = default
# 		self.cache = LFUCache(self.maxsize, self.ttl, self.timer, self.default)


# 	def add_item(self, key, value, ttl=None):
# 		self.cache.add(key, value, ttl)



# 	def get_value(self, key):
# 		return self.cache.get(key)


# if __name__ == "__main__":
# 	cache1 = LFUCacheManage()
# 	cache1.add_item(1, 1)
# 	print('111111111')
# 	get()


"""*********单列模式********"""
import threading

class LFUCacheManage(object):
	_instance = None # 定义一个类属性初始值为None,在__new__方法中判断_instance是否为none,为none,则创建对象返回对象的引用super().__new__(cls)
	_is_init = False # 定义一个类属性初始值为False,判断是否初始化过,无则初始化,并将值重置为True，有则无需初始化
	_instance_lock = threading.Lock()
	def __init__(self, maxsize=None, ttl=None, timer=None, default=None):
		if not LFUCacheManage._is_init:
			print("后执行init方法")
			LFUCacheManage._is_init = True
			self.maxsize = maxsize
			self.ttl = ttl
			self.timer = timer
			self.default = default
			self.cache = LFUCache(self.maxsize, self.ttl, self.timer, self.default)

	def __new__(cls, *args, **kwargs):
		if LFUCacheManage._instance is None:
			with LFUCacheManage._instance_lock:
				if LFUCacheManage._instance is None:
					print("先执行new方法")
					LFUCacheManage._instance = super().__new__(cls)
		return LFUCacheManage._instance


	def add_item(self, key, value, ttl=None):
		self.cache.add(key, value, ttl)



	def get_value(self, key):
		return self.cache.get(key)

if __name__ == "__main__":
	obj1 = LFUCacheManage()
	obj2 = LFUCacheManage()
	print(obj1, obj2)
	print(obj1 is obj2)
