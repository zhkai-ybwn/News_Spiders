# -*- coding: utf-8 -*-
import hashlib
from scrapy.utils.project import get_project_settings
import os
from redis import StrictRedis
import datetime
CRAWLAB_ENV = True if os.environ.get('YAHOO_REDIS_HOST') else False


def md5(url):
    m = hashlib.md5()
    b = url.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5


def get_connection(settings):
    redis_host = settings.get("REDIS_HOST")
    redis_port = settings.get("REDIS_PORT")
    redis_params = settings.getdict('REDIS_PARAMS')
    redis_password = redis_params['password']
    redis_db = redis_params['db']
    with StrictRedis(host=redis_host, port=redis_port, password=redis_password, db=redis_db) as conn:
        return conn


def write_start_urls_into_redis(conn, key, value):
    conn.sadd(key, value)


def format_date(date_list):
    current_year = datetime.datetime.now().year
    date_str = str(current_year) + '/' + \
        date_list[0][0:date_list[0].find('(')] + ' ' + date_list[2]
    return datetime.datetime.strptime(date_str, '%Y/%m/%d %H:%M')


def format_date_china_daily(date_list):
    date_info = ''
    for i in range(0, len(date_list)):
        date_info = date_info + date_list[i].replace('', '').replace('\n', '')
    arr_info = date_info.split('|')
    len_info = len(arr_info)
    date_str = ''
    if len_info > 0:
        str_len = len(arr_info[len_info - 1])
        date_str = arr_info[len_info - 1].replace(" ", "")[8: str_len]
    return datetime.datetime.strptime(date_str, '%Y-%m-%d%H:%M')


def format_source_china_daily(date_list):
    date_info = ''
    for i in range(0, len(date_list)):
        date_info = date_info + date_list[i].replace('', '').replace('\n', '')
    arr_info = date_info.split('|')
    len_info = len(arr_info)
    source_str = ''
    if len_info > 0:
        for i in range(0, len_info - 1):
            source_str = source_str + arr_info[i]
    return source_str.strip()
