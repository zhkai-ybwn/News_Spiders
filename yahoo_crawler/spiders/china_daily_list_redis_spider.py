# -*- coding: utf-8 -*-
from scrapy import Request

import scrapy

from ..items.china_daily_list_redis_item import ChinaDailyListRedisItem


class ChinaDailyListRedisSpider(scrapy.Spider):
    name = 'china_daily_list_redis_spider'
    allowed_domains = ['chinadaily.com.cn']
    start_urls = ['http://www.chinadaily.com.cn/world/asia_pacific']

    custom_settings = {
        'ITEM_PIPELINES': {
            'yahoo_crawler.pipelines.redis_pipeline.RedisPipeline': 200
        },
        'DOWNLOADER_MIDDLEWARES': {
            'yahoo_crawler.middlewares.ProcessAllExceptionMiddleware': 201,
            'yahoo_crawler.middlewares.RandomDelayMiddleware': 202
        }
    }

    def parse(self, response):
        if response.status == 400 or response.status == 500:
            self.crawler.engine.close_spider(
                self, 'page is not found, close spider'
            )
        else:
            item = ChinaDailyListRedisItem()
            url_list = response.xpath(
                '//*[@id="left"]/div[@class="mb10 tw3_01_2 "]//a/@href').extract()
            for url in url_list:
                item['url'] = 'http:' + url
                yield item

