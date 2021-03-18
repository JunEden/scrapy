import scrapy
from eeee.items import EeeeItem
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
import logging
import re

class eeeeSpider(scrapy.Spider):
	name ='eeee'
	start_url = "https://www.1111.com.tw/search/job"
	def start_requests(self):
		queryStringList = [
			{
			'ks':'python',
			# 'd0':'140300',
			},
		]

		for queryString in queryStringList:

			yield FormRequest(url=self.start_url,method='GET', \
				formdata=queryString,callback=self.datail_requests)

	def datail_requests(self,response):
		all_ads = response.xpath('//*[@id="maincontent"]/div[1]/ul[1]/li/div/div[1]')
		for ads in all_ads:
			key = ads.re('<em>(.*?)</em>')[0]

		yield SplashRequest(response.request.url,self.deep_request, \
			meta={'url':response.request.url,'key':key},endpoint="render.html", \
			dont_filter=True,)


	def deep_request(self,response):
		url = response.meta.get('url')
		html = response.text
		amount = int(re.findall('<select.* / (.*?) 頁',html)[0])
		logging.info(amount)

		all_ads = response.xpath('//*[@id="maincontent"]/div[1]/ul[1]/li/div/div[1]')
		for ads in all_ads:
			key = ads.re('<em>(.*?)</em>')[0]
			key = response.meta.get('key')
			#logging.info(key)
		for page in range(1,amount+1):
			yield SplashRequest(url+"&page="+str(page), \
				endpoint='render.html',dont_filter=True,meta={'key':key})
	def parse(self,response):
		logging.info("into parse function")#增加提示
		#article去掉切片就可以取得所有標題
		jobs = response.xpath('//*[@id="maincontent"]/div[1]/ul[1]/li/div/div[1]')#
		#增加提示jobs找到幾個
		logging.info(len(jobs))
		html = response.text
		#先先遍歷關鍵字再去重--> 關鍵字變小 -->再去重一次最後拼接起來
		#pattern = response.xpath('//em').extract()
		#logging.info(pattern)
		#print(pattern)

		keyword = response.meta.get('key')
		logging.info(keyword)

		for job in jobs:
			item = EeeeItem()
			item['category'] = keyword
			item['name'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[1]/a/@title').get()
			
			#href因為是雙引號 所以直接用雙引號
			item['jobLink'] = "http:" + job.css('a').re('.*href="(.*?)" title=.*')[0]
			
			#用xpath把公司名稱跟取得出來用replace把後面切片掉
			item['company'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[3]/@aria-label').get()
			#用xpath取得後再用-1從後面擷取出來
			item['companyAddress'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[2]/a/@title').get().split("》")[-1]

			#擷取超連結出來
			item['companyLink'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[2]/a/@href').get()

			#抓取 工作區 需要年資 跟學歷
			item['jobArea'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[2]/a/@title').get().split("》")[-1]
			item['experience'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[4]/i[3]/@aria-label').get()
			item['school'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[4]/i[4]/@aria-label').get()

			item['description'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[5]/@title').get()
			item['salary'] = job.xpath('//*[@id="maincontent"]/div[1]/ul/li[1]/div[1]/div[1]/div[4]/i[2]/@aria-label').get()
			yield item