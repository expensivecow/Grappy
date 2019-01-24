import scrapy

class BaseSpider(scrapy.Spider):
    name = "quotes"
    downloadURLs = []

    def __init__(self, url_input=None, category='', **kwargs):
        if url_input is not None:
            self.start_urls = [url_input]
        else:
            print("**************************************")
            print("No Links to Query")
            print("**************************************")
        super().__init__(**kwargs)  # python3

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_directories = response.selector.xpath("//a[@class=\"js-navigation-open\"]/@href").extract()

        print("************")
        print(next_directories)
        print("************")
        print(len(next_directories))

        if (len(next_directories) > 0):
            file = open('./temp/test.txt', "w")
            for item in next_directories:
                file.write('https://github.com' + item + "\n")
            file.close()
        else:
            print("NO MORE DIRECTORIES")
