# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PchomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
	Brand = scrapy.Field()
	Productname = scrapy.Field()
	bikeimage = scrapy.Field()
	Introduction = scrapy.Field()
	value = scrapy.Field()

	def toDict(self):
		return {k:v for k,v in self._values.items()}
	def getList(self):
		return [v for v in self._values.values()]
	def getField(self):
		return [k for k in self._values.keys()]