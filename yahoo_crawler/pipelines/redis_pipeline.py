# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import redis
from ..items.redis_base_item import RedisBaseItem
import logging
import sys
CRAWLAB_ENV = True if os.environ.get('YAHOO_REDIS_HOST') else False


class RedisPipeline(object):
    def __init__(self, redis_host, redis_port, redis_password, redis_db):
        self.pool = redis.ConnectionPool(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            max_connections=10)

    @classmethod
    def from_crawler(cls, crawler):
        redis_host = crawler.settings.get('REDIS_HOST')
        redis_port = crawler.settings.get('REDIS_PORT')
        redis_params = crawler.settings.getdict('REDIS_PARAMS')
        redis_password = redis_params['password']
        redis_db = redis_params['db']
        return cls(redis_host, redis_port, redis_password, redis_db)

    def process_item(self, item, spider):
        if isinstance(item, RedisBaseItem) is False:
            return item
        try:
            self.conn = redis.Redis(connection_pool=self.pool)
            item.save(self.conn, item, spider)
        except Exception as e:
            logging.exception(sys.exc_info)
            logging.error('redis pipeline has problem:%s' % (e))
            spider.crawler.engine.close_spider(
                spider, 'redis pipeline has problem, spider interrupt')
        return item

    def close_spider(self, spider):
        self.pool.disconnect()
