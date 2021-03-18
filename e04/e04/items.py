# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class E04Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	category = scrapy.Field()
	name = scrapy.Field()
	jobLink = scrapy.Field()
	company = scrapy.Field()
	companyAddress = scrapy.Field()
	companyLink = scrapy.Field()
	jobArea = scrapy.Field()
	experience = scrapy.Field()
	school = scrapy.Field()
	description = scrapy.Field()
	salary = scrapy.Field()
	#字典表達式
	def toDict(self):
		return {k:v for k,v in self._values.items()}
	#取出值
	def getList(self):
		return [v for v in self._values.values()]
	#取出鍵#注意空白
	def getField(self):
		return [k for k in self._values.keys()]