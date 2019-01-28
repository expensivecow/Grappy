import scrapy
import time
import random
import requests
from lxml.html import fromstring

class BaseSpider(scrapy.Spider):
    name = "BaseSpider"
    projectURLs = []
    currentPagesScraped = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # python3

    def getSettings(self):
        print("Existing settings: %s" % self.settings.attributes.keys())

    def setMaxPages(self, numPages):
        self.maxPages = numPages

    def start_requests(self):
        print('hello world ' + str(len(self.start_urls)))
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def getNumProjectURLs(self):
        return self.numURLs

    def parse(self, response):
        if not response.xpath('//title'):
            yield scrapy.Request(url=response.url, dont_filter=True)
        
        parser = fromstring(response.text)
        next_page = parser.xpath("//a[@class=\"next_page\"]/@href")
        current_urls = parser.xpath("//a[@class=\"v-align-middle\"]/@href")

        for url in current_urls:
            project_url = 'https://github.com' + url
            self.projectURLs.append(project_url)

        if ((self.currentPagesScraped < self.maxPages) and len(next_page) == 1):
            next_url = 'https://github.com' + next_page[0]
            self.currentPagesScraped += 1
            print('current pages scraped %d' % self.currentPagesScraped)
            print('max pages %d' % self.maxPages)
            yield scrapy.Request(url = next_url, callback = self.parse)
