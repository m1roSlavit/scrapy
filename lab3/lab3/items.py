# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstituteItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class DepartmentItem(scrapy.Item):
    name = scrapy.Field()
    institute = scrapy.Field()
    link = scrapy.Field()


class ScientistItem(scrapy.Item):
    name = scrapy.Field()
    department = scrapy.Field()


class StaffItem(scrapy.Item):
    name = scrapy.Field()
    institute = scrapy.Field()
