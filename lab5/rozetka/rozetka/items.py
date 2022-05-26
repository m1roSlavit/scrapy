import scrapy


class RozetkaItem(scrapy.Item):
    model = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
