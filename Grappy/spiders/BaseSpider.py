import scrapy
import time
import random
import requests
from lxml.html import fromstring

class BaseSpider(scrapy.Spider):
    name = "BaseSpider"
    projectURLs = []
    currentPagesScraped = 0

    def __init__(self, url_input=None, max_pages=None, category='', **kwargs):
        if url_input is not None:
            self.start_urls = [url_input]
        else:
            print("**************************************")
            print("No Links to Query")
            print("**************************************")

        if max_pages is not None:
            self.maxPages = max_pages
        else:
            self.maxPages = 50

        super().__init__(**kwargs)  # python3

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def getNumProjectURLs(self):
        return self.numURLs

    def parse(self, response):
        if not response.xpath('//title'):
            yield Request(url=response.url, dont_filter=True)
        
        parser = fromstring(response.text)
        next_page = parser.xpath("//a[@class=\"next_page\"]/@href")
        current_urls = parser.xpath("//a[@class=\"v-align-middle\"]/@href")

        for url in current_urls:
            project_url = 'https://github.com' + url
            self.projectURLs.append(project_url)

        if (len(next_page) == 1):
            next_url = 'https://github.com' + next_page[0]
            self.currentPagesScraped += 1
            yield scrapy.Request(url = next_url, callback = self.parse)
