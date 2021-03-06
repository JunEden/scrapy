import os
import csv
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
		self.__path = "../csvFile"
#檢查存不存在的方法 用os 裡的listdir去取
	def _Save__isExist(self,name):
		spCsv= [i for i in os.listdir(self.__path) if ".csv" in i and name in i]
		if spCsv:
			return True
		return False

	def _Save__createTable(self,name):
		obj = open(os.path.join(self.__path,name['category']+".csv"),"a+")
		writer = csv.writer(obj)
		#name比較特別要傳入整個item 不能只單單name
		#writerow 咖樂name寫入藥用整個getfield 不能只單單傳入name
		writer.writerow(name.getField())
		return writer

	def _Save__deDuplicate(self,item):
		with open(os.path.join(self.__path,item['category']+".csv"),"r") as f:
			data = [i.split(",")for i in f.readlines()]

		if [i[0] for i in data if item ['name'] in i]:
			return True
		return False

	def insert(self,item):
		if not self._Save__isExist(item['category']):
			writer = self._Save__createTable(item)

		else:
			writer = csv.writer(open(os.path.join(self.__path,item['category']+".csv"),"a+"))
			if self._Save__deDuplicate(item):
				return False
			writer.writerow(item.getList())
			logging.info("csv: insert data success")
			return True

