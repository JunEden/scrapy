from scrapy import cmdline

cmdline.execute('scrapy crawl pchome -o items.json -s FEED_EXPORT_ENCODING=utf-8'.split())