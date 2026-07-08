import scrapy


class ProductPriceItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    source_site = scrapy.Field()
