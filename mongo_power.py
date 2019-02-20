'''此模块封装mongo数据库'''
from pymongo import MongoClient #导入pymongo模块

class MyMongo():
	"""此类封装pymongo,更加便捷高效使用"""
	def __init__(self,host='localhost',port=27017,db_name=None,collection_name=None):
		self.host=host
		self.port=port
		self.db_name=db_name
		self.collection_name=collection_name
		try:
			#创建连接对象(位置传参)
			self.conn=MongoClient(self.host,self.port)
			print("数据库连接成功")
		except Exception as e:
			print("数据库连接失败:",e)
		try:
			#创建数据库对象(无此数据库，则创建，有则切换至此数据库)
			self.db=self.conn.self.db_name
			#self.db=self.conn[self.db_name]
			print("数据库对象创建成功")
		except Exception as e:
			print("数据库对象创建失败:",e)
		try:
			#创建集合对象(无此集合，则创建，有则切换至此集合)
			self.myset=self.db.self.collection_name
			#self.myset=self.db[self.collection_name]
			print("创建集合对象成功")
		except Exception as e:
			print("创建集合对象失败:",e)

	def insert_one_data(self,mongo_cmd):
		"""此方法为插入单条数据,示意如下
		{'name':"张铁林",'King':'乾隆'}
		"""
		try:
			self.myset.insert_one(mongo_cmd)
			print("数据插入成功")
		except Exception as e:
			print("数据插入失败:",e)

	def insert_many_data(self,mongo_cmd_list):
		"""此方法为插入多条数据,示意如下
		[{'name':'张国立','King':'康熙'},{'name':'陈道明','King':'康熙'}]
		"""
		try:
			self.myset.insert_many(mongo_cmd_list)
			print("数据插入成功")
		except Exception as e:
			print("数据插入失败:",e)

	def update_one_data(self,mongo_cmd):
		"""此方法更新查询的一条数据"""
		try:
			self.myset.update_one(mongo_cmd)
			print("数据更新成功")
		except Exception as e:
			print("数据更新失败:",e)

	def update_many_data(self,mongo_cmd):
		"""此方法更新查询的所有数据"""
		try:
			self.myset.update_many(mongo_cmd)
			print("数据更新成功")
		except Exception as e:
			print("数据更新失败:",e)

	def delete_one_data(self,mongo_cmd):
		"""此方法删除查询的一条数据"""
		try:
			self.myset.delete_one(mongo_cmd)
			print("数据删除成功")
		except Exception as e:
			print("数据删除失败:",e)

	def delete_many_data(self,mongo_cmd):
		"""此方法删除查询的所有数据"""
		try:
			self.myset.delete_many(mongo_cmd)
			print("数据删除成功")
		except Exception as e:
			print("数据删除失败:",e)

	def find_data(self,find_condition):
		"""此方法为查询数据"""
		#返回的cursor为结果集的列表形式,每个结果遍历即可
		try:
			cursor=self.myset.find(find_condition)
			print("数据查询成功")
		except Exception as e:
			print("数据查询失败:",e)
		# print(cursor.next()) #取下一个值
		# print(cursor.count()) #统计数量
		# print(cursor.limit(2)) #取前几个文档
		# print(cursor.skip(2))  #跳过前几个文档
		for i in cursor:
			print(i)


if __name__ == "__main__":
	mymongo=MyMongo('localhost',27017,'mongotest','mongotest')
# 	def create_database(self):
# 		"""此方法创建数据库或者切换指定数据库"""
# 		conn=MongoClient(host=self.host,port=self.port)
# #创建数据库连接
# conn=MongoClient("localhost",27017)

# #创建数据库对象
# db=conn.database_myself  #库名是database_myself

# #创建集合对象
# myset=db.collection_myself  #database_myself中的集合collection_myself

#通过集合的对象(myset)进行相应的数据操作
#进行增删改查等一系列操作
#插入操作
# myset.insert({'name':"张铁林",'King':'乾隆'})
# myset.insert([{'name':'张国立','King':'康熙'},{'name':'陈道明','King':'康熙'}])
#查找操作
# cursor = myset.find({'age':{'$gt':15}},{'_id':0})
# for i in cursor:
#     print(i)
# print(cursor.next()) #取下一个值
# print(cursor.count()) #统计数量
# print(cursor.limit(2)) #取前几个文档
# print(cursor.skip(2))  #跳过前几个文档

#关闭链接
# conn.close()