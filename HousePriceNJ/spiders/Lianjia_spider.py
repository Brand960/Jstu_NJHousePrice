# -*- coding: UTF-8 -*-
import scrapy
from HousePriceNJ.items import Houseprice_nj

class LianjiaSpider(scrapy.spiders.Spider):
    name="Lianjia"
    allowed_domains = ["nj.fang.lianjia.com"]
    start_urls = ["https://nj.fang.lianjia.com/loupan"]

    def parse(self, response):
        pg=1
        url_list=[]
        totalPage=response.xpath('//div[@class="list-wrap"]/div/@page-data').extract()[0].split(":")[1].split(",")[0]
        totalPage=int(totalPage)
        while(pg<totalPage):
            url_list.append("https://nj.fang.lianjia.com/loupan/pg"+str(pg))
            #print("https://nj.fang.lianjia.com/loupan/pg"+str(pg))
            pg+=1  
        #print(url_list)
        for url in url_list:
            yield scrapy.Request(url,callback=self.parse_html)


    def parse_html(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
            #f.write(response.body)

        for sel in response.xpath('//ul/li'):
            item=Houseprice_nj()
            item["name"]=sel.xpath('//ul/li[@data-index="0"]/div[@class="info-panel"]/div[@class="col-1"]/h2/a/text()').extract()
            item["price"]=sel.xpath('//ul/li[@data-index="0"]/div[@class="info-panel"]/div[@class="col-2"]/div[@class="price"]/div/span/text()').extract()
            item["location"]=sel.xpath('//ul/li[@data-index="0"]/div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span/text()').extract()
            item["area"]=sel.xpath('//ul/li[@data-index="0"]/div[@class="info-panel"]/div[@class="col-1"]/div[@class="area"]/span/text()').extract()
            
        yield item