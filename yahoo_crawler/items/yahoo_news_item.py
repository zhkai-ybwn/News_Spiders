# -*- coding: utf-8 -*-
from .elasticsearch_base_item import ElasticSearchBaseItem
import scrapy
from ..tool.common_util import md5


class YahooNewsItem(ElasticSearchBaseItem):
    crawlab_spider_name = scrapy.Field()
    crawlab_task_id = scrapy.Field()
    datasoure = scrapy.Field()  # 新闻来源
    url = scrapy.Field()  # 新闻链接
    publish_date = scrapy.Field()  # 新闻发布时间
    title = scrapy.Field()  # 新闻标题
    content = scrapy.Field()  # 新闻正文内容

    def get_index(self):
        return 'yahoo_news'

    def save(self, es_client, item, crawlab_task_id):
        item['crawlab_task_id'] = crawlab_task_id
        data = dict(item)
        es_client.index(index=self.get_index(), body=data, id=md5(item['url']))
