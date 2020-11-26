"""
cacheout 模块使用 cacheout类型：FIFO,LIFO,LRU,MRU,LFU,PR
此模块只对与LFUCache(最少使用优先剔除)
"""

from cacheout import LFUCache

cache = LFUCache(maxsize=4, ttl=None, timer=None, default=None)
# maxsize: 存储的条目数量(一个键值对)当数量超过4条最少使用的剔除掉，当频率相同时最先缓存的最先剔除掉
# ttl: 过期时间秒为单位(默认不过期)
# timer:

# 添加单条cache.add(key, value, ttl=None)
cache.add(1,1)

# 添加多条cache.add_many({key1:value1,key2:value2}, ttl=None)
cache.add_many({2:2, 3:3, 4:4}, ttl=None)

# cache.clear()清除所有缓存
cache.clear()

# cache.configure(maxsize=None, ttl=None, timer=None, default=None) 全局级别的缓存配置
cache.configure(maxsize=None, ttl=None, timer=None, default=None)

# cache.copy()返回缓存的副本

# cache.delete(key)删除缓存键并返​​回已删除的条目数（1<存在>或0<不存在>)

# delete_expired()删除过期的缓存键并返​​回删除的条目数

# delete_many(itert) 一次删除多个缓存键 itert可以是list, str, re.compile(), function

# cache.evict()根据缓存替换策略执行缓存逐出,首先，删除所有过期的条目.然后，使用缓存替换策略删除非TTL条目;删除非TTL条目时，此方法将仅删除最小条目数以减少下面的条目数maxsize。如果maxsize为0，则只会删除过期的条目

# cache.expire_times()返回TTL密钥的缓存过期

# cache.expired(key, expires_on=None) 返回缓存密钥是否过期

# cache.full()返回缓存是否已满

# cache.get(key, default=None)返回缓存值键或默认或者missing(key)如果它不存在或已过期

# cache.get_many(iter)作为dict由iteratee过滤的键/值对中的一个，返回许多缓存值，该值可以是以下之一:list,str,re.compile(),function

# cache.has(key)返回缓存键是否存在并且尚未过期

# cache.iterms()返回所有缓存的条目

# cache.keys()返回所有缓存的key

# cache.memoize(*, ttl=None, typed=False) 装饰器将函数包装为带有备忘录的可调用函数，并在同步和异步函数上均起作用。

# cache.popitem()根据缓存替换策略删除并返回下一个缓存项，而忽略到期时间（即，要弹出的项的选择仅基于缓存键顺序）。(key, value)

# cache.set(key, value, ttl=None)设置缓存键/值并替换任何以前设置的缓存键。如果先前存在高速缓存密钥，则对其进行设置会将其移到高速缓存堆栈的末尾，这意味着它将最后被逐出

# cache.set_many(items, ttl=None)一次设置多个缓存键。项目（dict）–要设置的缓存键/值的映射

# cache.size()返回缓存条目的数量

# cache.values()所有缓存的缓存值value



for i in range(1, 10):
	cache.add(i, i)

cache.get(1)
cache.get(3)
# cache.clear()
keys = cache.keys()
print(keys)