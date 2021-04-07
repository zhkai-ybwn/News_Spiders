import scrapy

class RedisBaseItem(scrapy.Item):
    """
    redis 基础方法
    """
    def get_redis_key(self):
        pass
    def save(self, conn, item, spider):
        pass