import pymysql
from datetime import datetime
from multiprocessing import Pool
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = ''
port = 3306
user = 'root'
password = ''
database = ''
engine = create_engine("")

def get_query(time_tuple):
	# engine.dispose()
	conn = engine.connect()
	print(conn)
	sql_cmd = "SELECT * FROM `` WHERE app_id=4 and res_date BETWEEN '%s' AND '%s';" % (time_tuple[0], time_tuple[-1])
	result_ls = conn.execute(sql_cmd).fetchall()
	print("子进程: %s, 查询结果条数: %s" % (os.getpid(), len(result_ls)))

if __name__ == '__main__':
	p = Pool(8)
	time_list = [('2020-03-22', '2020-04-22'), ('2020-04-22', '2020-05-22'), ('2020-05-22', '2020-06-22'), ('2020-06-22', '2020-07-22'), ('2020-07-22', '2020-08-22'), ('2020-08-22', '2020-09-22'),('2020-09-22', '2020-10-22'),  ('2020-10-22', '2020-11-22')]
	begin_time = datetime.now()
	for i in time_list:
		p.apply_async(func=get_query, args=(i, ))
	p.close()
	p.join()
	end_time = datetime.now()
	print("等待所有子进程所用时间: %s" % (end_time - begin_time).seconds)