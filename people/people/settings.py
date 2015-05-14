# -*- coding: utf-8 -*-

# Scrapy settings for people project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'people'

SPIDER_MODULES = ['people.spiders']
NEWSPIDER_MODULE = 'people.spiders'

DOWNLOAD_DELAY = 0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'people (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
    'scrapy_mongodb.MongoDBPipeline']

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'my_items'
MONGODB_SPIDER_NAME = True
