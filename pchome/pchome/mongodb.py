import pymongo
import logging
from pchomedao import Save

def singletonDecorator(cls,*args,**kwargs):
	instance = {}
	def wrapperSingleton(*args,**kwargs):
		if cls not in instance:
			instance[cls] =cls(*args,**kwargs)
			logging.info('new instance')
		return instance[cls]
	return wrapperSingleton

@singletonDecorator
class database(Save):
	def __init__(self):
		self.__connection = pymongo.MongoClient("localhost",27017)
		self.__db = self.__connection.pchome
		#檢查存在跟創建
	def _Save__isExist(self,name):
		return True
	def _Save__createTable(self,name):
		return True

	def _Save__deDuplicate(self,item):
		collections = self.__db[item['Brand']]
		result = collections.find_one({'Productname':item['Productname']})
		if result:
			return True
		return False
		#上面檢查有無重複 沒有再接下來插入
	def insert(self,item):
		if not self._Save__deDuplicate(item):
			collections = self.__db[item['Brand']]
			collections.insert(item.toDict())
			logging.info("Mongo: insert data success")
			return True
		return False

	def close(self):
		self.__connection.close()
