# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KijijiItem(scrapy.Item):
    # define the fields for your item here like:
    ad_id = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    date_posted = scrapy.Field()
