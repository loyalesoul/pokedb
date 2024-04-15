# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from scrapy.pipelines.images import FilesPipeline
from pathlib import Path
from urllib.parse import urlparse
import pymongo
from itemadapter import ItemAdapter

LOG_LEVEL = "INFO"


class PokemonFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return "artworks/" + Path(urlparse(request.url).path).name


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
        self.db[self.collection_name].create_index("national_no", unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Use update_one with upsert=True to perform an upsert operation
        self.db[self.collection_name].update_one(
            {"national_no": item["national_no"]},
            {"$set": ItemAdapter(item).asdict()},
            upsert=True,
        )
        return item
