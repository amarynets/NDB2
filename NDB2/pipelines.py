# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi

class MySQLPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)

        return d
    def _do_upsert(self, conn, item, spider):
        insert = """ INSERT INTO notebook (url, properties, price, title, image) 
        VALUES (%s, %s, %s, %s, %s)"""
        data = (
            item['url'],
            item['properties'],
            item['price'],
            item['title'],
            item['image']
        )
        conn.execute(insert, data)

    def _handle_error(self, failure, item, spider):        
        # do nothing, just log
        log.err(failure)