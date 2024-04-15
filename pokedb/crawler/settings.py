# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# BOT_NAME = "googlebot"


SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "crawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "crawler.middlewares.CrawlerSpiderMiddleware": 543,
# }

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# settings.py
FILES_STORE = "s3://pokemon/"
IMAGE_STORE = ".storage"

RETRY_TIMES = 3

# Timeout settings
DOWNLOAD_TIMEOUT = 5  # Timeout for requests in seconds

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DATABASE = "pokedb"
AWS_ENDPOINT_URL = "http://127.0.0.1:9000"
IMAGES_STORE_S3_ACL = "public-read"
AWS_ACCESS_KEY_ID = "minioadmin"
AWS_SECRET_ACCESS_KEY = "minioadmin"

FEEDS = {"s3://pokemon/pokemon_list.json": {"format": "jsonlines"}}

LOG_LEVEL = "DEBUG"
COOKIES_ENABLED = False

SPIDERMON_ENABLED = True

EXTENSIONS = {
    "spidermon.contrib.scrapy.extensions.Spidermon": 500,
}

SPIDERMON_MIN_ITEMS = 1025
SPIDERMON_MAX_ITEM_VALIDATION_ERRORS = 1
SPIDERMON_MAX_ERRORS = 1
SPIDERMON_MAX_WARNINGS = 100
SPIDERMON_MAX_DOWNLOADER_EXCEPTIONS = 10

# SPIDERMON_VALIDATION_SCHEMAS = {
#     PokemonItem: 'crawler/schemas/pokemon_item.json',
# }

SPIDERMON_ADD_FIELD_COVERAGE = True

SPIDERMON_VALIDATION_ADD_ERRORS_TO_ITEMS = True

SPIDERMON_DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1229277713974693928/TtUOOjUWh5t3EKhKmZ6Z89c5TXaZPrGOqd7hng2K3mkm9AmAffY_P9LtzL6J5C9Ty8sY"
