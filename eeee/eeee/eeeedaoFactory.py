from eeeeEnum import InputType

#接下來建立工廠class 會有個方法會用inputtype判斷來獲取實體
class factory:
	#T是傳入pipelines總類
	def getInstance(self,t):
		if t == InputType.mongodb:
			from mongodb import database
			return database()

		elif t == InputType.mysql:
			from mysqldb import database
			return database()

		elif t == InputType.csv:
			from csvstore import database
			return database()

		else:
			return None