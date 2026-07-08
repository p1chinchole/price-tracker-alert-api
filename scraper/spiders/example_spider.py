import scrapy

from scraper.items import ProductPriceItem


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/"]

    def parse(self, response):
        item = ProductPriceItem()
        item["name"] = "Example Product"
        item["url"] = response.url
        item["price"] = "99.99"
        item["source_site"] = "example"
        yield item
