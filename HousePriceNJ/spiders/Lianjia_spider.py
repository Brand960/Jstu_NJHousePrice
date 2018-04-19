# -*- coding: UTF-8 -*-
import json
import scrapy
import requests
from HousePriceNJ.items import Houseprice_nj
from HousePriceNJ.settings import ak, api


class LianjiaSpider(scrapy.spiders.Spider):
    name = "Lianjia"
    allowed_domains = ["nj.fang.lianjia.com", "nj.lianjia.com"]

    # start_urls = ["https://nj.fang.lianjia.com/loupan/pg/pg1"]

    def start_requests(self):
        yield scrapy.Request("https://nj.fang.lianjia.com/loupan/pg/pg1", self.parse_newhouse)
        yield scrapy.Request("https://nj.lianjia.com/ershoufang/pg/pg1", self.parse_oldhouse)

    def parse_newhouse(self, response):
        for url in response.xpath('//a[@class="resblock-img-wrapper"]/@href').extract():
            each_url = "https://nj.fang.lianjia.com" + url
            yield scrapy.Request(each_url, self.parse_html_newhouse)

        totalPage = int(
            response.xpath('/html/body/div[@class="page-box"]/@data-total-count').extract()[0]) // 10
        curPage = int(
            response.xpath('//div[@class="filter-container"]/@data-selected').extract()[0].split('"page":')[1].split(
                ',"pagesize"')[0]
        )
        # while(pg<totalPage):
        #     url_list.append("https://nj.fang.lianjia.com/loupan/pg"+str(pg))
        #     pg+=1
        # url_list.append("https://nj.fang.lianjia.com/loupan/pg" + str(1))
        if curPage < totalPage:
            nextpage = "https://nj.fang.lianjia.com/loupan/pg/pg" + str(curPage + 1)
            yield scrapy.Request(nextpage, self.parse_newhouse)

    def parse_oldhouse(self, response):
        for url in response.xpath('//div[@class="title"]/a/@href').extract():
            yield scrapy.Request(url, self.parse_html_oldhouse)

        totalPage = int(
            response.xpath("//div[@class='page-box fr']/div/@page-data").extract()[0].split('{"totalPage":')[1].split(
                ',"curPage"')[0])

        curPage = int(
            response.xpath("//div[@class='page-box fr']/div/@page-data").extract()[0].split('"curPage":')[1].split("}")[
                0])
        # while(pg<totalPage):
        #     url_list.append("https://nj.fang.lianjia.com/loupan/pg"+str(pg))
        #     pg+=1
        # url_list.append("https://nj.fang.lianjia.com/loupan/pg" + str(1))
        if curPage < totalPage:
            nextpage = "https://nj.lianjia.com/ershoufang/pg/pg" + str(curPage + 1)
            yield scrapy.Request(nextpage, self.parse_oldhouse)

    def parse_html_newhouse(self, response):
        """
        解析每一个房产信息的详情页面，生成item
        :param response:
        :return:
        """
        baidu_url = api + "&ak=" + ak
        item = Houseprice_nj()
        item["name"] = response.xpath('//h1/text()').extract()[0]
        if response.xpath('//p[@class="where "]/span/text()').extract():
            item["location"] = "南京" + response.xpath('//p[@class="where "]/span/text()').extract()[0].split("：")[1]
        elif response.xpath('//p[@class="where manager"]/span/text()').extract():
            item["location"] = "南京" + response.xpath('//p[@class="where manager"]/span/text()').extract()[0].split("：")[
                1]
        else:
            item["location"] = "南京" + response.xpath(
                '//p[@class="where"]/span/text()').extract()[0]
        if response.xpath('//p[@class="when "]/span/text()').extract():
            item["when"] = response.xpath('//p[@class="when "]/span/text()').extract()[1]
        elif response.xpath('//p[@class="when manager"]/span/text()').extract():
            item["when"] = response.xpath('//p[@class="when manager"]/span/text()').extract()[1]
        else:
            item["when"] = response.xpath('//p[@class="when"]/span/text()').extract()[1]

        if response.xpath('//span[@class="junjia"]/text()').extract():
            item["price"] = response.xpath('//span[@class="junjia"]/text()').extract()[0]
        else:
            item["price"] = 0
        # locations = list(item["location"])
        # for location in locations:
        url = baidu_url + "&address=" + item["location"]
        CordinateXY = requests.get(url).json()["result"]["location"]
        # lng.append(CordinateXY["lng"])
        # lat.append(CordinateXY["lat"])
        item["lng"] = CordinateXY["lng"]
        item["lat"] = CordinateXY["lat"]

        yield item

    def parse_html_oldhouse(self, response):
        """
        解析每一个二手房产信息的详情页面，生成item
        :param response:
        :return:

        """
        baidu_url = api + "&ak=" + ak
        item = Houseprice_nj()
        item["name"] = response.xpath('//div[@class="communityName"]/a/text()').extract()[0]
        if response.xpath('//div[@class="communityName"]/a/text()').extract():
            item["location"] = "南京" + response.xpath('//div[@class="communityName"]/a/text()').extract()[0]
        if response.xpath('//div[@class="introContent"]//div[@class="content"]/ul/li[1]/span[2]/text()').extract():
            item["when"] = \
                response.xpath('//div[@class="introContent"]//div[@class="content"]/ul/li[1]/span[2]/text()').extract()[
                    0]
        if response.xpath('//span[@class="unitPriceValue"]/text()').extract():
            item["price"] = int(response.xpath('//span[@class="unitPriceValue"]/text()').extract()[0])
        else:
            item["price"] = 0
        # locations = list(item["location"])
        # for location in locations:
        url = baidu_url + "&address=" + item["location"]
        CordinateXY = requests.get(url).json()["result"]["location"]
        # lng.append(CordinateXY["lng"])
        # lat.append(CordinateXY["lat"])
        item["lng"] = CordinateXY["lng"]
        item["lat"] = CordinateXY["lat"]

        yield item
