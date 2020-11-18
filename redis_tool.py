"""
redis 数据库
pip install redis
"""

import redis
import certifi


# 简单连接
def simple_connent():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')

# ssl证书验证连接
def connect_by_ssl():
    r = redis.Redis(host='xxxxxx.cache.amazonaws.com', port=6379, db=0, ssl=True, ssl_ca_certs='/etc/ssl/certs/ca-certificates.crt')
    r.set('foo', 'bar')

# ssl证书验证连接
def connect_byssl2():
    r = redis.Redis(host='xxxxxx.cache.amazonaws.com', port=6379, db=0, ssl=True, ssl_ca_certs=certifi.where())
    r.set('foo', 'bar')

# redis池连接
def connect_pools():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    r.set('foo', 'bar')

# 管道操作
def pipe_handle():
    r = redis.Redis()
    pipe = r.pipeline()
    pipe.set('foo', 'bar')
    pipe.get('bing')
    pipe.execute()  # [True, b'baz']








