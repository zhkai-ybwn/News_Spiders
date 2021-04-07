import scrapy

class ElasticSearchBaseItem(scrapy.Item):
    def get_index(self):
        pass
    def save(self, es_client, item):
        pass