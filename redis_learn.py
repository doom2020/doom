import redis
import time


def connect_redis():
    # connect methods(Redis(child class), StrictRedis(father class))
    r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=False)
    # r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_response=True)
    r.set('name', 'yuanzhijian')
    print(r.get('name'))


def connect_pool():
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=redis_pool)
    r.set('name', 'chengbing')
    print(r.get('name'))


def redis_pipeline():
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=redis_pool)
    pipe = r.pipeline(transaction=True)
    r.set('name', 'yuan')
    r.set('age', '10')
    print(r.get('name'))
    print(r.get('age'))
    pipe.execute()
    print('------------')
    print(r.get('name'))
    print(r.get('age'))


def redis_str_operation():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    # r.set('name', 'yuan', ex=3)
    # print(r.get('name'))
    # time.sleep(3)
    # print(r.get('name'))
    # r.setex('age', 3, '10')
    # print(r.get('age'))
    # time.sleep(4)
    # print(r.get('age'))
    # r.mset(dict(name='yuan', age='10'))
    # print(r.mget(('name', 'age')))
    # r.set('name', 'yuan')
    # print(r.getset('name', 'zhi'))
    # print(r.get('name'))
    # print(r.getrange('name', 0, 1))
    # r.setrange('name', 1, 'x')
    # print(r.get('name'))
    # r.setrange('name', 6, 'zzzzzzz')
    # print(r.get('name'))
    r.set('name', 'yuan')
    print(r.strlen('name'))
    r.append('name', 'zhijian')
    print(r.get('name'))


def redis_hash_operation():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    r.hset('yuanzhijian', 'age', '10')
    print(r.hget('yuanzhijian', 'age'))
    print(r.hgetall('yuanzhijian'))
    r.hmset('yuanzhijian', dict(age=10, like='play'))
    print(r.hgetall('yuanzhijian'))
    print(r.hlen('yuanzhijian'))
    print(r.hkeys('yuanzhijian'))
    print(r.hvals('yuanzhijian'))
    print(r.hexists('yuanzhijian', 'height'))
    print(r.hexists('yuanzhijian', 'age'))
    print(r.hdel('yuanzhijian', 'age'))
    print(r.hkeys('yuanzhijian'))


def redis_list_operation():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    r.lpush('number', 1, 2, 3)
    r.lpush('number', 5, 6, 7)
    # r.rpush('like', 'eat', 'play', 'sleep')
    # r.lpushx('number', 8)
    # r.rpushx('like', 'run')
    print(r.llen('like'))
    print(r.llen('number'))
    # r.linsert('number', 3, 10, 12)
    # r.lrem('like', 1, 4)
    print(r.lpop('number'))
    print(r.lindex('number', 5))


def redis_set_operation():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    r.delete('number')
    r.sadd('number', 1)
    r.sadd('number', 1, 2)
    print(r.smembers('number'))
    print(r.scard('number'))
    print(r.sismember('number', 1))
    print(r.spop('number'))


def redis_order_set_operation():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    r.zadd('score', dict(a1=1, a2=2, a3=3))
    print(r.zcard('score'))
    print(r.exists('score'))


class RedisHelp(object):
    def __init__(self):
        # connect
        self.conn = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        # define name
        self.channel = 'monitor'

    def publish(self, msg):
        self.conn.publish(self.channel, msg)
        return True

    def subscribe(self):
        pub = self.conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub

    @staticmethod
    def publish_task(obj):
        import time
        import random
        while True:
            time.sleep(random.randint(1, 5))
            obj.publish('hello')

    @staticmethod
    def subscribe_task(obj):
        redis_sub = obj.subscribe()
        while True:
            msg = redis_sub.parse_response()
            print(msg)


if __name__ == "__main__":
    redis_order_set_operation()
    # redis_hash_operation()
    # redis_str_operation()
    # import threading
    # connect_redis()
    # connect_pool()
    # redis_pipeline()
    # obj = RedisHelp()
    # t1 = threading.Thread(target=obj.publish_task, args=(obj, ))
    # t2 = threading.Thread(target=obj.subscribe_task, args=(obj, ))
    # t1.start()
    # t2.start()

