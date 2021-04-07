# -*- coding: utf-8 -*-
import scrapy
from ..items.yahoo_list_redis_item import YahooNewsListRedisItem
from scrapy import Request


class YahooNewsListRedisSpider(scrapy.Spider):
    name = 'yahoo_news_list_redis_spider'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['https://www.yahoo.co.jp/']

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
                self, 'page is not found, close spider')
        else:
            item = YahooNewsListRedisItem()
            url_list = response.xpath(
                '//*[@id="tabpanelTopics1"]/div/div[1]/ul//a/@href').extract()
            for url in url_list:
                yield Request(url=url, dont_filter=True, callback=self.parse_url)

    def parse_url(self, response):
        url = response.xpath(
            '//*[@id="contentsWrap"]/article/div[2]/div/p/a/@href').extract_first()
        yield Request(url=url, dont_filter=True, callback=self.parse_detail_url)

    def parse_detail_url(self, response):
        item = YahooNewsListRedisItem()
        item['url'] = response.url
        yield item
