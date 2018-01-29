# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#房名、地址、价格、价格/平方、户型面积
class Houseprice_nj(scrapy.Item):
    name=scrapy.Field()
    location=scrapy.Field()
    # cordinate=scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    price=scrapy.Field()
    when=scrapy.Field()
