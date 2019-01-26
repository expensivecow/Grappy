import sys
import scrapy
from spiders import ProjectSpider as Spider
from spiders import BaseSpider as BaseSpider
from scrapy.crawler import CrawlerProcess
import os
import random
import requests
from lxml.html import fromstring

#---------------- DEFINED VARIABLES BGN ----------------#
#---------------- DEFINED VARIABLES END ----------------#

def main():
	mainDir = os.path.dirname(os.path.realpath(__file__))
	with open(mainDir + '/config/singularTest.txt') as staticFile:
		staticLinks = staticFile.readlines()

		for row in staticLinks:
			data = row.strip()
			data = data.split(",")

			if len(data) != 2:
				raise Exception("Missing data for record. Please double check configuration.")

			language = data[0]
			link = data[1]

			performBaseProjectScrape(downloadDirectory = mainDir + '/temp/projects/', language = language, link = link)
			#reupdateProxies(mainDir)
			#---------------- SCRAPE INDIVIDUAL PROJECT URLS BGN ----------------#
			'''
			urls = [
            	'https://github.com/shakacode/react-webpack-rails-tutorial'
            	#'https://github.com/shakacode/react-webpack-rails-tutorial/blob/master/spec/factories.rb'
        	]

			spider = Spider.ProjectSpider(url_input = urls)
			#print(spider.urls)

			process.crawl(spider, start_urls = urls)
			process.start() # the script will block here until the crawling is finished

			print("********* FINAL SPIDER URLS *********")
			print(spider.downloadURLs)
			print("********* FINAL SPIDER URLS *********")
			'''
			#---------------- SCRAPE INDIVIDUAL PROJECT URLS END ----------------#

def performBaseProjectScrape(downloadDirectory, language, link):
	process = CrawlerProcess({
	    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
	})

	baseSpider = BaseSpider.BaseSpider()
	print(baseSpider.maxPages)
	urls = ['https://github.com/search?l=JavaScript&o=desc&q=language%3AC&s=&type=Repositories']
	process.crawl(baseSpider, start_urls = urls)
	process.start()

	if (baseSpider.projectURLs is not None):
		file = open(downloadDirectory+language+'Projects.txt', 'w')
		file.truncate(0)

		for url in baseSpider.projectURLs:
			file.write(url+'\n')

		print('saving projects to' + downloadDirectory+language+'Projects.txt' + '\n')
		file.close()

def reupdateProxies(mainDir):
	url = 'https://free-proxy-list.net/'
	response = requests.get(url)
	parser = fromstring(response.text)
	proxies = []
	f = open(mainDir + '/config/proxylist.txt', 'w')
	f.truncate(0)
	for i in parser.xpath('//tbody/tr'):
		if i.xpath('.//td[7][contains(text(),"yes")]'):
			proxy = "https://" + ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
			f.write(proxy + '\n')
	f.close()
	return proxies

if __name__== "__main__":
  main()
