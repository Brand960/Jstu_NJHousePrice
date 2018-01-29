# -*- coding: UTF-8 -*-
import json
import scrapy
import requests
from HousePriceNJ.items import Houseprice_nj
from HousePriceNJ.settings import ak, api


class LianjiaSpider(scrapy.spiders.Spider):
    name = "Lianjia"
    allowed_domains = ["nj.fang.lianjia.com"]
    start_urls = ["https://nj.fang.lianjia.com/loupan"]

    def parse(self, response):
        for url in response.xpath('//a[@data-xftrack=10138]/@href').extract():
            url2 = "https://nj.fang.lianjia.com" + url
            yield scrapy.Request(url2, self.parse_html)

        totalPage = int(
            response.xpath('//div[@class="list-wrap"]/div/@page-data').extract()[0].split(":")[1].split(",")[0])
        curPage = int(
            response.xpath('//div[@class="list-wrap"]/div/@page-data').extract()[0].split(":")[2].split("}")[0])
        # while(pg<totalPage):
        #     url_list.append("https://nj.fang.lianjia.com/loupan/pg"+str(pg))
        #     pg+=1
        # url_list.append("https://nj.fang.lianjia.com/loupan/pg" + str(1))
        if curPage < totalPage:
            nextpage = "https://nj.fang.lianjia.com/loupan/pg" + str(curPage + 1)
            yield scrapy.Request(nextpage, self.parse)

    def parse_html(self, response):
        """
        解析每一个房产信息的详情页面，生成item
        :param response:
        :return:
        """
        baidu_url = api + "&ak=" + ak
        item = Houseprice_nj()

        # for sel in response.xpath('//ul/li[@data-index="0"]'):
        #     lng = []
        #     lat = []
        item["name"] = response.xpath('//h1/text()').extract()[0]
        item["price"] = response.xpath('//span[@class="junjia"]/text()').extract()[0]

        if response.xpath('//p[@class="where "]/span/text()').extract():
            item["location"] = "南京" + response.xpath('//p[@class="where "]/span/text()').extract()[0].split("：")[1]
        else:
            item["location"] = "南京" + response.xpath('//p[@class="where manager"]/span/text()').extract()[0].split("：")[
                1]

        # locations = list(item["location"])
        # for location in locations:
        url = baidu_url + "&address=" + item["location"]
        CordinateXY = requests.get(url).json()["result"]["location"]
        # lng.append(CordinateXY["lng"])
        # lat.append(CordinateXY["lat"])
        item["lng"] = CordinateXY["lng"]
        item["lat"] = CordinateXY["lat"]
        if response.xpath('//p[@class="when "]/span/text()').extract():
            item["when"] = response.xpath('//p[@class="when "]/span/text()').extract()[1]
        else:
            item["when"] = response.xpath('//p[@class="when manager"]/span/text()').extract()[1]

        yield item
