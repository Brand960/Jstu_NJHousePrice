# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from openpyxl import workbook

class HousepricenjPipeline(object):
    def __init__(self):
        host=settings['MONGODB_URL']
        port=settings['MONGODB_PORT']
        dbname=settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)

        # 定义数据库
        db = client[dbname]
        self.table = db[settings['MONGODB_TABLE']]

    def process_item(self, item, spider):
        data = dict(item)
        self.table.insert(data)
        # line = [item['name'], item['location'], str(item['price']), item['lng'], item['lat'],item['area']]


        return item