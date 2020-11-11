from gevent import monkey

monkey.patch_all()  # 必须写在最上面，这句话后面的所有阻塞全部能够识别了

import gevent  # 直接导入即可
import time

def eat():
    # print()　　
    print('eat food 1')
    time.sleep(2)  # 加上monkey就能够识别到time模块的sleep了
    print('eat food 2')

def play():
    print('play 1')
    time.sleep(1)  # 来回切换，直到一个I/O的时间结束，这里都是我们个gevent做得，不再是控制不了的操作系统了。
    print('play 2')

g1 = gevent.spawn(eat)
g2 = gevent.spawn(play)
gevent.joinall([g1, g2])  # 或者g1.join() g2.join()
print('主')