# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy.pipelines.images import FilesPipeline
from pathlib import PurePosixPath
from urllib.parse import urlparse
import pymongo
from itemadapter import ItemAdapter

LOG_LEVEL = "INFO"


class PokemonFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return "artworks/" + PurePosixPath(urlparse(request.url).path).name


class PokemonURLsPipeline:
    def process_item(self, item, spider):
        if "pokemon_urls" not in spider.state:
            spider.state["pokemon_urls"] = []
        spider.state["pokemon_urls"].append(item["pokemon_url"])
        return item


class MongoPipeline:
    collection_name = "pokemon"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
