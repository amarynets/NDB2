# -*- coding: utf-8 -*-
import scrapy
from NDB2.items import NDB2


class Ndb2spiderSpider(scrapy.Spider):
    name = "NDB2"
    allowed_domains = ["price.ua"]
   
    start_urls = [
        "http://price.ua/catc839t14.html?price[min]=5000&price[max]=140749"
    ]

    def parse(self, response):
        
        for product in response.xpath("//div[contains(@class,'product-item-wrap')]"):
            item = NDB2()
            item['title']=product.xpath(".//a[contains(@class,'model-name')]/text()").extract()
            item['url']=product.xpath(".//a[contains(@class,'model-name')]/@href").extract()

            description=[]
            for div in product.xpath(".//div[@class='characteristics']/div/div[@class='item']"):
                description.append(div.xpath("./text()").extract()[0].strip()+' '+div.xpath("./span/text()").extract()[0].strip())
            item['properties']= ' '.join(map(str, description))
            item['image'] = product.xpath('.//div[@class="photo-wrap"]/a/span/span/img/@data-original').extract()

            item['price'] = str(product.xpath('.//div[@class="price-wrap"]/span/text()').extract_first()).replace("\xa0", "")
                 
            yield item
            
            #item['url'] = str(response.xpath('./a[contains(@class,"model-name")]/@href').extract())
            #item['image'] = str(response.xpath('//div[@class="photo-wrap"]/a/span/span/img/@data-original').extract())
            #item['title'] = str(response.xpath('.//a[contains(@class,"model-name")]/text()').extract())
