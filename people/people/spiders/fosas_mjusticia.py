from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from people.items import FosaItem

class FosasMinisterioSpider(Spider):
    name = "mjusticia"
    allowed_domains = ["mapadefosas.mjusticia.es"]
    start_urls = []

    base_url = "http://mapadefosas.mjusticia.es/exovi_externo/CargarDetalleFosa.htm?fosaId=#ID#",  
    for i in range(1,2199):
        start_urls.append(base_url.replace('#ID#',str(i)))

    def parse(self, response):

        fosa = FosaItem()
        fosa['url'] = response.url
        fosa['codigo'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[1]/dl/dd[1]/text()').extract()

        return fosa