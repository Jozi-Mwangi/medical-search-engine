import scrapy


class DiseasespiderSpider(scrapy.Spider):
    name = "diseasespider"
    allowed_domains = ["https://www.health.harvard.edu/a-through-c"]
    start_urls = ["https://www.health.harvard.edu/a-through-c"]

    def parse(self, response):
        diseases = response.xpath("//p/strong")
        descriptions = response.xpath('//p/text()')

        
        pass
