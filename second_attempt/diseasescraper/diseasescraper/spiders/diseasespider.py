import scrapy


class DiseasespiderSpider(scrapy.Spider):
    name = "diseasespider"
    allowed_domains = ["dph.illinois.gov"]
    start_urls = ["https://dph.illinois.gov/topics-services/diseases-and-conditions/diseases-a-z-list.html"]

    def parse(self, response):
        pass
