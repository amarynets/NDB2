# -*- coding: utf-8 -*-
import scrapy
from NDB2.items import NDB2
from scrapy.selector import HtmlXPathSelector

class Ndb2spiderSpider(scrapy.Spider):
    name = "NDB2"
    allowed_domains = ["price.ua"]
    urls = []
    urls.append("http://price.ua/catc839t14/page1.html?price[min]=5000&price[max]=140749")
    for i in range(2, 3):
        link = "http://price.ua/catc839t14/page" + str(i) + ".html?price[min]=5000&price[max]=140749"
        urls.append(link)
    "http://price.ua/catc839t14/page1.html"
    start_urls = urls

    def parse(self, response):
        
      
        for product in response.xpath("//div[contains(@class,'product-item-wrap')]"):
            item = NDB2()
            
            #Don't delete
            #
            try:
                item['image'] = product.xpath('//div[@class="white-wrap clearer-block"]//img/@src').extract_first()
                item['title'] = product.xpath(".//a[contains(@class,'model-name')]/text()").extract()
                price = product.xpath('.//div[@class="price-wrap"]/span/text()').extract_first()
                item['price'] = int(str(price).replace("\xa0", ""))
                description = []
                for div in product.xpath(".//div[@class='characteristics']/div/div[@class='item']"):
                    description.append(div.xpath("./text()").extract()[0].strip()+' '+div.xpath("./span/text()").extract()[0].strip())
                item['properties'] = str(description)
                item['url'] = product.xpath(".//a[contains(@class,'model-name')]/@href").extract()
            except:
                price = product.xpath(".//a[contains(@class,'ga_card_mdl_price')]/text()").extract_first()
                item['price'] = int(str(price).replace("\xa0", ""))
                item['properties'] = product.xpath('.//span[@class="wrap-descr"]/text()').extract_first()
                item['title'] = product.xpath('.//div[@class="photo-wrap"]//a//span/img/@title').extract_first()
                item['image'] = product.xpath('.//div[@class="photo-wrap"]//a//span/img/@data-original').extract_first()
                item['url'] = None
            yield item