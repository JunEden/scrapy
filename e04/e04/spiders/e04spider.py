import scrapy
from e04.items import E04Item
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
import logging
import re

class e04Spider(scrapy.Spider):
		name = 'e04'
		#覆蓋原有scrapy的方法
		start_url = "https://www.104.com.tw/jobs/search"
		def start_requests(self):
			queryStringList = [
				{
				'keyword':'java',
				'area':'6001001000%2C6001002000',
				},
			]
			#先抓取動態頁面
			for queryString in queryStringList:
				yield FormRequest(url=self.start_url,method='GET', \
					formdata=queryString,callback=self.detail_requests)
		#先寫一次splash_request 參數帶下去 用splash_request 那response.request.url會自動GET到Dcker內的IP跟PO號的組合
		def detail_requests(self,response):
			yield SplashRequest(response.request.url,self.deep_request, \
				meta={'url':response.request.url},endpoint='render.html', \
				dont_filter=True)
				#dont_filter避免scrapy過濾相似的請求


				
			#先寫deep_request模塊,處理爬取幾頁的function
		def deep_request(self,response):
			#先取得上面得到的url,response被從上面送下來後字帶get屬性
			url = response.meta.get('url')
			#取得網頁meta的數據原始碼
			html = response.text
			#我們是要計算頁數所以轉成int計算頁數
			amount = int(re.findall('<meta.*－(.*?) 個工作機會.*',html)[0])#會有兩個一樣地所以取一個就好
			page = int(amount / 20) + 1
			#加一個提示訊息
			logging.info(page)

			#
			for page in range(1,page+1):#用range跑一遍這邊page用range是因為不產生子級
				yield SplashRequest(url+"&page="+str(page), \
					endpoint='render.html',dont_filter=True)#endpoint一樣用render 這邊沒有用到Lua腳本

			#這邊先不寫callback function 遍歷完處理完介面後就直接進入parser處理資料

		def parse(self,response):
			logging.info("into parse function")#增加提示
			#article去掉切片就可以取得所有標題
			jobs = response.xpath('//*[@id="js-job-content"]/article/div[1]')#
			#增加提示jobs找到幾個
			logging.info(len(jobs))
			html = response.text
			#先關鍵字去叢把EM內取得出來 字母變小 在去叢一次最後拼接起來
			pattern = re.compile('<em.*?ht">(.*?)</em>',re.S)
			print(pattern)
			keyword = "".join(set([i.lower() if i.isalpha() else i for i in set(pattern.findall(html))]))
			logging.info(keyword)

			for job in jobs:
				item = E04Item()
				item['category'] = keyword
				item['name'] = job.css('a').re('.*get="_blank">(.*?)</a>')[0].replace('<em class="b-text--highlight">','').replace('</em>','')
				
				#href因為是雙引號 所以直接用雙引號
				item['jobLink'] = "http:" + job.css('a').re('.*href="(.*?)" class=.*')[0]
				
				#用xpath把公司名稱跟取得出來用replace把後面切片掉
				item['company'] = job.xpath('//*[@id="js-job-content"]/article[5]/div[1]/ul[1]/li/a/text()').get().split()
				#用xpath取得後再用-1從後面擷取出來
				item['companyAddress'] = job.xpath('ul[1]/li/a/@title').get().split("：")[-1]

				#擷取超連結出來
				item['companyLink'] = job.xpath('ul[1]/li/a/@href').get()

				#抓取 工作區 需要年資 跟學歷
				item['jobArea'] = job.xpath('ul[2]/li[1]/text()').get()
				item['experience'] = job.xpath('ul[2]/li[2]/text()').get()
				item['school'] = job.xpath('ul[2]/li[3]/text()').get()

				item['description'] = job.xpath('./p/text()').get()
				item['salary'] = job.xpath('./div/span/text()').get()
				yield item