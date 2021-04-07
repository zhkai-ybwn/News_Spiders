# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
import logging
import random
import time

class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTION = (
        defer.TimeoutError,
        TimeoutError,
        DNSLookupError,
        ConnectionRefusedError,
        ConnectionDone,
        ConnectError,
        ConnectionLost,
        TCPTimedOutError,
        ResponseFailed,
        IOError,
        TunnelError
    )
    def process_response(self, request, response, spider):
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            logging.error('response(%s) status is: %s' % (response.url, response.status))
            response = HtmlResponse(url = request.url, status = 400)
        return response
    
    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.ALL_EXCEPTION):
            logging.error('Got exception: %s' % (exception))
            response = HtmlResponse(url = request.url, status = 500)
            return response
        logging.error('not contained exception: %s'%exception)


class RandomDelayMiddleware(object):
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        delay = crawler.spider.settings.get('RANDOM_DELAY', 10)
        if not isinstance(delay, int):
            raise ValueError('RANDOM_DELAY new a int')
        return cls(delay)

    def process_request(self, request, spider):
        delay = random.randint(0, self.delay)
        time.sleep(delay)
