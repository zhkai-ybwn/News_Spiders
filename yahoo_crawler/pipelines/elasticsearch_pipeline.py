# -*- coding: utf-8 -*-
from elasticsearch.connection import create_ssl_context
import ssl
from elasticsearch import Elasticsearch
import os
from ..items.elasticsearch_base_item import ElasticSearchBaseItem
import logging
import sys
CRAWLAB_ENV = True if os.environ.get('CRAWLAB_MONGO_HOST') else False

class ElasticSearchPipeline(object):
    def __init__(self, es_host, es_username, es_password):
        self.es_client = Elasticsearch(es_host,
            http_auth=(es_username, es_password),
            scheme="https",
            port=443,
            maxsize=10,
            verify_certs=False,)

    @classmethod
    def from_crawler(cls, crawler):
        es_host = os.environ.get('YAHOO_ES_HOST') if CRAWLAB_ENV else crawler.settings.get('ES_HOST')
        es_username = os.environ.get('YAHOO_ES_USERNAME') if CRAWLAB_ENV else crawler.settings.get('ES_USERNAME')
        es_password = os.environ.get('YAHOO_ES_PASSWORD') if CRAWLAB_ENV else crawler.settings.get('ES_PASSWORD')
        return cls(es_host, es_username, es_password)

    def process_item(self, item, spider):
        try:
            if isinstance(item, ElasticSearchBaseItem) is False:
                return item
            crawlab_task_id = os.environ.get('CRAWLAB_TASK_ID') if CRAWLAB_ENV else 'LOCAL_TASK'
            item.save(self.es_client, item, crawlab_task_id)
        except Exception as e:
            logging.exception(sys.exc_info())
            logging.error('elasticsearch pipeline has problem: %s' % (e))
            spider.crawler.engine.close_spider(spider, 'elasticsearch pipeline has problem, spider interrupt!')
        return item
