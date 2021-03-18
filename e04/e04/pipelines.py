# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from e04Enum import InputType
from e04daoFactory import factory
import logging
from scrapy.exceptions import DropItem
#DropItem阻止item被儲存 如果發現重複會把item丟掉 不會中斷程式執行

fac = factory()

class MYSQLPipeline:
	def __init__(self):
		self.db = fac.getInstance(InputType.mysql)
	def process_item(self,item,spider):
		result = self.db.insert(item)
		if not result:
			raise DropItem("MYSQL: %s is duplicated"%item['name'])
		return item
	def __del__(self):
		self.db.close()
		logging.info("mysql connection close...")


class MONGOPipeline:
	def __init__(self):
		self.db = fac.getInstance(InputType.mongodb)
	def process_item(self,item,spider):
		result = self.db.insert(item)
		if not result:
			raise DropItem("Mongo: %s is duplicated"%item['name'])
		return item
	def __del__(self):
		self.db.close()
		logging.info("mongodb connection close...")


class CSVPipeline:
	def __init__(self):
		self.db = fac.getInstance(InputType.csv)
	def process_item(self,item,spider):
		result = self.db.insert(item)
		if not result:
			raise DropItem("CSV: %s is duplicated"%item['name'])
		return item
