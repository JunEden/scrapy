import scrapy
from pchome.items import PchomeItem
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
import logging
import re
import json
from urllib import parse

class pchomeSpider(scrapy.Spider):
	name ='pchome'
	start_url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?"
	def start_requests(self):
		queryStringList = [
			{
			'q':r"%E6%91%A9%E6%89%98%E8%BB%8A%",
			},
		]
		for queryString in queryStringList:
			for page in range(1,11):
				queryString['page'] = str(page)
				yield FormRequest(url=self.start_url,method='GET', \
					formdata= queryString)


	def parse(self,response):
		logging.info("into parse function")#增加提示
		commoditys = response.text
		#print(commoditys)
		commoditys = json.loads(commoditys)
		#commoditys = Jsonre
		
		#(parse.unquote('%'+commoditys['token'][0]))
		#commoditys = commoditys['prods']

		for commodity in commoditys['prods']:
			item = PchomeItem()
			#print(commodity)
			item['Brand'] =  'Motorcycle'
			item['Productname'] = commodity['name']					
			item['bikeimage'] = "https://c.ecimg.tw" + commodity['picS']			
			item['Introduction'] = commodity['describe']
			item['value'] = commodity['originPrice']
			yield item
