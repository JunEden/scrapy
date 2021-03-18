import pymysql
import logging
from e04dao import Save

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
		#初始化資料庫連接
		config = {
			'host':'127.0.0.1',
			'port':3306,
			'user':'root',
			'password':'a123456',
			'db':'e04',
		}
		#connection控制游標用
		self.__connection = pymysql.connect(**config)
	#檢查表存不存在
		#私有屬性 模塊名子前有__就要加上抽象class的名子
	def _Save__isExist(self,name):
		#創建游標後with確保動作做完自己關閉
		with self.__connection.cursor() as cursor:
			
			cursor.execute('show tables;')
			#fetchall抓住所有結果
			result = cursor.fetchall()
			#如果我name在任何結果裡面就會return 不然就回傳False
			if [i for i in result if name in i]:
				return True
			return False
	#自動創建表
	def _Save__createTable(self,name):
		with self.__connection.cursor() as cursor:
			sql = "create table %s(jobname varchar(255),jobLink varchar(255),company varchar(255),companyAddress varchar(255),companyLink varchar(255),jobArea varchar(255),experience varchar(255),school varchar(255),description varchar(255), salary varchar(255));" %name
			#最好加個try知道中間發生什麼錯誤
			try:
				cursor.execute(sql)
			except Exception as e:
				logging.info(e)
				self.__connection.rollback()
				return False

			else:
				logging.info("create table %s" %name)
				self.__connection.commit()
				return True
	#檢查item有無重複
	def _Save__deDuplicate(self,item):
		with self.__connection.cursor() as cursor:
			cursor.execute('select * from %s where jobname="%s"'%(item['category'],item['name']))
			result = cursor.fetchall()
			if [ i for i in result if item['name']in i ]:
				return True
			return False

	def insert(self,item):
		if not self._Save__isExist(item['category']):
			result = self._Save__createTable(item['category'])
			if not result:
				return False
		with self.__connection.cursor() as cursor:
			if self._Save__deDuplicate(item):
				return False
			logging.info(item.getList())
			sql = 'insert into %s values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(item['category'],item['name'],item['jobLink'],item['company'],item['companyAddress'],item['companyLink'],item['jobArea'],item['experience'],item['school'],item['description'],item['salary'])#把值轉換成元祖傳入到裡面
			try:
				cursor.execute(sql)
			except Exception as e:
				logging.info(e)
				self.__connection.rollback()

			else:
				logging.info("insert data:%s success" %item['name'])
				self.__connection.commit()
				return True

	def close(self):
		self.__connection.close()