# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from ..tool.common_util import get_connection, write_start_urls_into_redis, format_date_china_daily, format_source_china_daily
from ..items.china_daily_item import ChinaDailyItem


class ChinaDailySpider(RedisSpider):
    name = 'china_daily_spider'
    redis_key = ''
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'SCHEDULER_PERSIST': True,
        'SCHEDULER_IDIE_BEFORE_CLOSE': 10,
        'REDIS_ENCOING': 'utf-8',
        'REDIS_START_URLS_AS_SET': True,
        'IDLE_NUMBER': 5,
        'MYEXT_ENABLED': True,
        'ITEM_PIPELINES': {
            'yahoo_crawler.pipelines.elasticsearch_pipeline.ElasticSearchPipeline': 200,
        },
        'EXTENSIONS': {
            'yahoo_crawler.redis_spider_close_exensions.RedisSpiderCloseExensions': 201
        },
        'DOWNLOADER_MIDDLEWARES': {
            'yahoo_crawler.middlewares.ProcessAllExceptionMiddleware': 202,
            'yahoo_crawler.middlewares.RandomDelayMiddleware': 203
        }
    }
    conn = None

    def _set_crawler(self, crawler):
        if self.conn is None:
            self.conn = get_connection(crawler.settings)
        return super()._set_crawler(crawler)

    def __init__(self, *args, **kwargs):
        self.redis_key = 'china_daily:start_urls'
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ChinaDailySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.status == 400 or response.status == 500:
            self.crawler.engine.close_spider(
                self, 'page is not found, close spider'
            )
            write_start_urls_into_redis(
                self.conn,
                self.redis_key + '_parsing_failed',
                response.url
            )
        else:
            item = ChinaDailyItem()
            item['datasoure'] = format_source_china_daily(response.xpath(
                '//*[@id="lft-art"]/div[1]/span[1]//text()').extract())
            item['url'] = response.url
            item['publish_date'] = format_date_china_daily(response.xpath(
                '//*[@id="lft-art"]/div[1]/span[1]//text()').extract())
            item['title'] = response.xpath(
                '//*[@id="lft-art"]/h1//text()').extract_first()
            item['content'] = response.xpath(
                '//*[@id="Content"]//text()').extract()
            yield item
