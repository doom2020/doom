'''此模块封装mysql数据库/表的建立以及增删改查操作'''

import pymysql

class MysqlHelper():
	"""此类封装mysql数据库"""
	def __init__(self,host='localhost',port=3306,user='root',password='123456',db=None,charset="utf8"):
		self.host=host
		self.user=user
		self.password=password
		self.port=port
		self.db=db
		self.charset=charset
		#创建数据库连接对象(关键字传参)
		self.connect=pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,db=self.db,charset=self.charset)
		#创建游标对象
		self.cursor=self.connect.cursor()

	def create_database(self,db_name):
		"""此方法创建数据库"""
		try:
			self.cursor.execute("drop database if exists %s"% db_name)
			self.cursor.execute("create database %s character set utf8"% db_name)
			self.connect.commit()
			print("创建数据库成功")
		except Exception as e:
			print("创建数据库失败:",e)

	def create_table(self,db_name,table_name,create_table_sql_cmd):
		"""此方法创建表"""
		try:
			self.cursor.execute("use %s"% db_name)
			self.cursor.execute("drop table if exists %s"% table_name)
			self.cursor.execute(create_table_sql_cmd)
			self.connect.commit()
			print("创建表成功")
		except Exception as e:
			print("创建表失败:",e)

	def insert_data(self,sql_cmd):
		"""此方法插入,更新,删除数据"""
		print("开始插入数据")
		try:
			self.cursor.execute(sql_cmd)
			self.connect.commit()
			print("数据插入成功")
		except Exception as e:
			print("插入数据出错:",e)
			self.connect.rollback()

	def find_data(self,sql_cmd):
		"""此方法查找数据"""
		print("开始查找数据")
		try:
			self.cursor.execute(sql_cmd)
			# 获取所有行的数据信息(列表的形式)
			result_list=self.cursor.fetchall()
			for result in result_list:
				print(result)
		except Exception as e:
			print("获取数据失败:",e)

	def close_connect(self):
		"""此方法关闭数据库连接"""
		self.cursor.close()
		self.connect.close()

if __name__ == "__main__":
	print("创建类的实例")
	mysql_helper=MysqlHelper()
	print("创建类的实例成功")
	mysql_helper.create_database('sqltest')
	create_table_sql_cmd="create table sqltest(id tinyint(5) unsigned primary key auto_increment,name varchar(20),pwd varchar(20))character set utf8"	
	mysql_helper.create_table('sqltest','sqltest',create_table_sql_cmd)


