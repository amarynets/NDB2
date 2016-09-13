# -*- coding: utf-8 -*-
import scrapy
from NDB2.items import NDB2


class Ndb2spiderSpider(scrapy.Spider):
    name = "NDB2"
    allowed_domains = ["price.ua"]
    urls = []
    urls.append("http://price.ua/catc839t14.html?price[min]=5000&price[max]=140749")
    for i in range(2, 11):
        link = "http://price.ua/catc839t14/page" + str(i) + ".html?price[min]=5000&price[max]=140749"
        urls.append(link)
    #"http://price.ua/catc839t14/page1.html"
    start_urls = urls

    def parse(self, response):
        
        for product in response.xpath("//div[contains(@class,'product-item-wrap')]"):
            item = NDB2()
            item['title']=product.xpath(".//a[contains(@class,'model-name')]/text()").extract()
            item['url']=product.xpath(".//a[contains(@class,'model-name')]/@href").extract()

            description=[]
            for div in product.xpath(".//div[@class='characteristics']/div/div[@class='item']"):
                description.append(div.xpath("./text()").extract()[0].strip()+' '+div.xpath("./span/text()").extract()[0].strip())
            item['properties']= str(description)
            item['image'] = product.xpath('//div[@class="white-wrap clearer-block"]//img/@src').extract_first()

            price = product.xpath('.//div[@class="price-wrap"]/span/text()').extract_first()
            if price == None:
                item['price'] = None
            else:
                item['price'] = int(str(price).replace("\xa0", ""))
                 
            yield item
            
            #item['url'] = str(response.xpath('./a[contains(@class,"model-name")]/@href').extract())
            #item['image'] = str(response.xpath('//div[@class="photo-wrap"]/a/span/span/img/@data-original').extract())
            #item['title'] = str(response.xpath('.//a[contains(@class,"model-name")]/text()').extract())
