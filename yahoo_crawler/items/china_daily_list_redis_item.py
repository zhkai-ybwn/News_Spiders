# -*- coding: utf-8 -*-

import scrapy
from .redis_base_item import RedisBaseItem
import hashlib
from scrapy.utils.python import to_bytes
from w3lib.url import canonicalize_url


class ChinaDailyListRedisItem(RedisBaseItem):
    url = scrapy.Field()

    def save(self, conn, item, spider):
        fp = hashlib.sha1()
        fp.update(to_bytes(canonicalize_url(item['url'])))
        unique_info = fp.hexdigest()
        added = conn.sadd('china_daily:dupefilter', unique_info)
        if added != 0:
            conn.sadd('china_daily:start_urls', item['url'])
