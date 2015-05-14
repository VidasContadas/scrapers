from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from people.items import FosaItem, VictimaItem
from scrapy.selector import HtmlXPathSelector

class VictimasMinisterioSpider(Spider):
    name = "mjusticia_victimas"
    allowed_domains = ["mapadefosas.mjusticia.es"]
    start_urls = []
    base_url = "http://mapadefosas.mjusticia.es/exovi_externo/CargarDetalleFosa.htm?fosaId=#ID#"
    for i in range(1,10):
        start_urls.append(base_url.replace('#ID#',str(i)))

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//*[@class="bloqueTablaResultadosConScroll"]/table//table[@class="tablehd"]/tr')
        
        for row in rows:
            victima = VictimaItem()
            cells = row.select('td/text()').extract()
            victima['nombre'] = cells[0]           
            victima['apellido'] = cells[1]                   
            victima['fosa'] = cells[2]

            #print victima
            yield victima
