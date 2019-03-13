# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem


class CleaningDataPipeline(object):
    def process_item(self, item, spider):
        item['price'] = item['price'].replace(' $', '')
        item['title'] = item['title'].replace('\n                                ', '')
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('room_items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['ad_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['ad_id'])
            return item


class KijijiPipeline(object):

    def process_item(self, item, spider):
        return item
