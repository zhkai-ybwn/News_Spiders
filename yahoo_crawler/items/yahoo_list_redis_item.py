# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from .redis_base_item import RedisBaseItem
import hashlib
from scrapy.utils.python import to_bytes
from w3lib.url import canonicalize_url


class YahooNewsListRedisItem(RedisBaseItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()

    def save(self, conn, item, spider):
        fp = hashlib.sha1()
        fp.update(to_bytes(canonicalize_url(item['url'])))
        unique_info = fp.hexdigest()
        added = conn.sadd('yahoo:dupefilter', unique_info)
        if added != 0:
            conn.sadd('yahoo:start_urls', item['url'])

