import pymysql
from datetime import datetime
from multiprocessing import Process
import gevent
from threading import Thread


def handle(sql_list):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='testdb', charset='utf8')
    cursor = conn.cursor()
    for sql_content in sql_list:
        try:
            cursor.execute(sql_content)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
            break



# 使用多进程(4个进程)
# if __name__ == "__main__":
#     with open(r'C:\Users\mi\Desktop\proxies\proxies.txt', 'r', encoding='utf8') as fr:
#         lines = fr.readlines()
#     need_lines = lines[0:10000]
#     sql_list = []
#     index = 1
#     for line in lines:
#         id = index
#         ip = line.split(',')[0].split(':')[-1]
#         port = line.split(',')[1].split(':')[-1]
#         _type = line.split(',')[3].split(':')[-1]
#         location = line.split(',')[-3].split(':')[-1]
#         response_time = line.split(',')[-2].split(':')[-1]
#         last_used_time = line.split(',')[-1]
#         date = last_used_time.split(' ')[0].split(':')[-1]
#         time = last_used_time.split(' ')[-1].replace('\n', '')
#         date_time = date + ' ' + time
#         date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
#         sql_content = "INSERT INTO `testdb`.`kuai_proxy` (`id`,`ip`, `port`, `type`, `location`, `response_time`, `last_used_time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (id, ip, port, _type, location, response_time, date_time)
#         sql_list.append(sql_content)
#         index += 1
#     sql_list1 = sql_list[0:2500]
#     sql_list2 = sql_list[2500:5000]
#     sql_list3 = sql_list[5000:7500]
#     sql_list4 = sql_list[7500:10000]
#     begin_time = datetime.now()
#     p1 = Process(target=handle, args=(sql_list1,))
#     p2 = Process(target=handle, args=(sql_list2,))
#     p3 = Process(target=handle, args=(sql_list3,))
#     p4 = Process(target=handle, args=(sql_list4,))
#     p_list = [p1, p2, p3, p4]
#     for p in p_list:
#         p.start()
#     for p in p_list:
#         p.join()
#     end_time = datetime.now()
#     used_time = (end_time - begin_time).seconds
#     print("执行时间: %s 秒" % used_time) # 147秒

# 使用协程(4个协程)
# if __name__ == "__main__":
#     with open(r'C:\Users\mi\Desktop\proxies\proxies.txt', 'r', encoding='utf8') as fr:
#         lines = fr.readlines()
#     need_lines = lines[0:10000]
#     sql_list = []
#     index = 1
#     for line in lines:
#         id = index
#         ip = line.split(',')[0].split(':')[-1]
#         port = line.split(',')[1].split(':')[-1]
#         _type = line.split(',')[3].split(':')[-1]
#         location = line.split(',')[-3].split(':')[-1]
#         response_time = line.split(',')[-2].split(':')[-1]
#         last_used_time = line.split(',')[-1]
#         date = last_used_time.split(' ')[0].split(':')[-1]
#         time = last_used_time.split(' ')[-1].replace('\n', '')
#         date_time = date + ' ' + time
#         date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
#         sql_content = "INSERT INTO `testdb`.`kuai_proxy` (`id`,`ip`, `port`, `type`, `location`, `response_time`, `last_used_time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (id, ip, port, _type, location, response_time, date_time)
#         sql_list.append(sql_content)
#         index += 1
#     sql_list1 = sql_list[0:2500]
#     sql_list2 = sql_list[2500:5000]
#     sql_list3 = sql_list[5000:7500]
#     sql_list4 = sql_list[7500:10000]
#     begin_time = datetime.now()
#     g1 = gevent.spawn(handle, sql_list1)
#     g2 = gevent.spawn(handle, sql_list2)
#     g3 = gevent.spawn(handle, sql_list3)
#     g4 = gevent.spawn(handle, sql_list4)
#     gevent.joinall([g1,g2,g3,g4])
#     end_time = datetime.now()
#     used_time = (end_time - begin_time).seconds
#     print("执行时间: %s 秒" % used_time) # 294秒

# 使用多线程(4个线程)
if __name__ == "__main__":
    with open(r'C:\Users\mi\Desktop\proxies\proxies.txt', 'r', encoding='utf8') as fr:
        lines = fr.readlines()
    need_lines = lines[0:10000]
    sql_list = []
    index = 1
    for line in lines:
        id = index
        ip = line.split(',')[0].split(':')[-1]
        port = line.split(',')[1].split(':')[-1]
        _type = line.split(',')[3].split(':')[-1]
        location = line.split(',')[-3].split(':')[-1]
        response_time = line.split(',')[-2].split(':')[-1]
        last_used_time = line.split(',')[-1]
        date = last_used_time.split(' ')[0].split(':')[-1]
        time = last_used_time.split(' ')[-1].replace('\n', '')
        date_time = date + ' ' + time
        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        sql_content = "INSERT INTO `testdb`.`kuai_proxy` (`id`,`ip`, `port`, `type`, `location`, `response_time`, `last_used_time`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (id, ip, port, _type, location, response_time, date_time)
        sql_list.append(sql_content)
        index += 1
    sql_list1 = sql_list[0:2500]
    sql_list2 = sql_list[2500:5000]
    sql_list3 = sql_list[5000:7500]
    sql_list4 = sql_list[7500:10000]
    begin_time = datetime.now()
    t1 = Thread(target=handle, args=(sql_list1,))
    t2 = Thread(target=handle, args=(sql_list2,))
    t3 = Thread(target=handle, args=(sql_list3,))
    t4 = Thread(target=handle, args=(sql_list4,))
    t_list = [t1, t2, t3, t4]
    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
    end_time = datetime.now()
    used_time = (end_time - begin_time).seconds
    print("执行时间: %s 秒" % used_time) # 143秒

# 单进程处理
# if __name__ == "__main__":
#     with open(r'C:\Users\mi\Desktop\proxies\proxies.txt', 'r', encoding='utf8') as fr:
#         lines = fr.readlines()
#     need_lines = lines[0:10000]
#     index_1 = 1
#     begin_time = datetime.now()
#     handle(need_lines, index_1)
#     end_time = datetime.now()
#     used_time = (end_time - begin_time).seconds
#     print("执行时间: %s 秒" % used_time) # 297秒