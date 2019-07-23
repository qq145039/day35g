# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class MongoPipeline():
    #开始爬取
    def open_spider(self,spider):
        self.client = MongoClient("mongodb://127.0.0.1:27017")
        self.db = self.client.xiao
    def process_item(self, item, spider):
        nei= item["nei"]
        zhang=item["zhang"]
        namebook=item["namebook"]
        category=item["category"]
        self.db.story.insert({"namebook": namebook, "category": category,"zhang":{"zh":zhang,"nei":nei,}})
    def close_spider(self,spider):
        self.client.close()

class Day35GPipeline(object):
    def process_item(self, item, spider):
        return item
