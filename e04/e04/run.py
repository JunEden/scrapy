from scrapy import cmdline

#這邊名子要跟settings裡的bot_name要一樣才會執行
cmdline.execute('scrapy crawl e04'.split())