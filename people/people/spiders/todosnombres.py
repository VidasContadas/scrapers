# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider


class todosnombresSpider(CrawlSpider):
    name = 'todosnombres'
    allowed_domains = ['todosnombres.org']
    start_urls = ['http://todosnombres.org/']
