# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging

LOG_LEVEL = "DEBUG"


class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            logging.info(f"Processing {item['image_urls']} for {item}")
            for image_url in item["image_urls"]:
                yield scrapy.Request(image_url, meta={"item": item})
        except Exception as e:
            logging.error(f"Error processing {item['image_urls']}: {e}")

    def file_path(self, request, response=None, info=None, *, item=None):
        try:
            # item = request.meta["item"]
            image_guid = request.url.split("/")[-1]
            path = f"full/{image_guid}"
            logging.info(f"Saving image at {path}")
            return path
        except Exception as e:
            logging.error(f"Error getting file path for {request.url}: {e}")
            return None

    def item_completed(self, results, item, info):
        try:
            image_paths = [x["path"] for ok, x in results if ok]
            if not image_paths:
                logging.warning(f"No images downloaded for {item['image_urls']}")
                raise DropItem("Item contains no images")
            item["image_paths"] = image_paths
            logging.info(f"Image paths: {image_paths}")
            return item
        except Exception as e:
            logging.error(f"Error completing item {item['image_urls']}: {e}")
            raise DropItem(f"Error completing item {item['image_urls']}: {e}")
