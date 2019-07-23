# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from day35g.items import Day35GItem


class QuSpider(CrawlSpider):
    name = 'qu'
    allowed_domains = ['www.quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.quanshuwang.com/'), callback='parse_item', follow=False),
    )
#获取类别
    def parse(self, response):
        x = response.xpath("//nav[@class='channel-nav']//li/a")
        for i in x:
            # print(i)
            z=i.xpath("./@href").extract()[0]
            category=i.xpath("./text()").extract()[0]
            yield scrapy.Request(z,self.parse2, meta={"category":category})
#获取小说
    def parse2(self, response):
        category = response.meta["category"]

        x = response.xpath("//section[@class='section board-list board-list-collapse']//li/a")
        for i in x:
            wn = i.xpath("./@href").extract()[0]
            namebook = i.xpath("./img/@alt").extract()[0]
            #print(wn,c)
            yield scrapy.Request(wn, self.parse3,meta={"namebook":namebook,"category":category})
            #进入目录
    def parse3(self,response):
        category = response.meta["category"]
        namebook = response.meta["namebook"]
        on = response.xpath("//div[@class='b-oper']/a/@href").extract()[0]

        yield scrapy.Request(on, self.parse4,meta={"namebook":namebook,"category":category})
        #得到小说名和章节
    def parse4(self,response):
        kd=response.xpath("//div[@class='chapterSo']")
        category = response.meta["category"]
        namebook = response.meta["namebook"]
        # name = kd.xpath("//strong/text()").extract()[0]
        # print(name)
        wang=kd.xpath("//div[@class='clearfix dirconone']/li/a")
        for i in wang:
            wan = i.xpath("./@href").extract()[0]
            zhang=i.xpath("./text()").extract()[0]
            #print(zhang,wan)
            yield scrapy.Request(wan, self.parse5,meta={"zhang":zhang,"namebook":namebook,"category":category})
#得到章节内容
    def parse5(self, response):
        x=response.xpath("//div[@class='mainContenr']")
        nei=x.xpath('string(.)').extract()[0]
        category = response.meta["category"]
        zhang=response.meta["zhang"]
        namebook=response.meta["namebook"]
        item =Day35GItem()
        item["nei"]=nei
        item["zhang"]=zhang
        item["namebook"] =namebook
        item["category"] =category
        yield item

