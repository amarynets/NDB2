# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class NDB2(Item):
    image = Field()
    brand = Field()
    title = Field()
    price = Field()
    properties = Field()
    url = Field()
