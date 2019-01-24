import sys
import scrapy
from spiders import BaseSpider as Spider
from scrapy.crawler import CrawlerProcess

def main():
	with open('./config/singularTest.txt') as staticFile:
		staticLinks = staticFile.readlines()
			

		process = CrawlerProcess({
		    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
		})

		for row in staticLinks:
			data = row.strip()
			data = data.split(",")

			if len(data) != 2:
				raise Exception("Missing data for record. Please double check configuration.")

			company = data[0]
			link = data[1]

			urls = [
            	#'https://github.com/shakacode/react-webpack-rails-tutorial'
            	'https://github.com/shakacode/react-webpack-rails-tutorial/blob/master/spec/factories.rb'
        	]

			spider = Spider.BaseSpider(url_input = urls)
			#print(spider.urls)

			process.crawl(spider, start_urls = urls)
			process.start() # the script will block here until the crawling is finished
			
			print(link)
  
if __name__== "__main__":
  main()
