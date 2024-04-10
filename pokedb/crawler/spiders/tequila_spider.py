from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TequilaSpider(CrawlSpider):
    name = "tequila"
    allowed_domains = ["ngoctequila.com"]
    start_urls = ["https://ngoctequila.com/"]

    rules = (
        Rule(
            LinkExtractor(allow_domains=allowed_domains),
            callback="parse_item",
            follow=True,
        ),
    )

    def parse_item(self, response):
        i = {}
        i["image_urls"] = response.css("img::attr(src)").getall()
        yield i
