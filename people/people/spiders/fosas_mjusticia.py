from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from people.items import FosaItem, VictimaItem


class FosasMinisterioSpider(Spider):
    name = "mjusticia_fosas"
    allowed_domains = ["mapadefosas.mjusticia.es"]
    start_urls = []

    base_url = "http://mapadefosas.mjusticia.es/exovi_externo/CargarDetalleFosa.htm?fosaId=#ID#"
    for i in range(1, 2199):
        start_urls.append(base_url.replace('#ID#',str(i)))

    def parse(self, response):

        fosa = FosaItem()
        fosa['url'] = response.url

        fosa['codigo'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[1]/dl/dd[1]/text()').extract()
        fosa['comunidad'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[1]/dl/dd[2]/text()').extract()
        fosa['provincia'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[1]/dl/dd[3]/text()').extract()
        fosa['municipio'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[1]/dl/dd[4]/text()').extract()
        fosa['latitud'] = response.xpath("//form[@id='formBuscador']//input[@name='latitudTx']/@value").extract()
        fosa['longitud'] = response.xpath("//form[@id='formBuscador']//input[@name='longitudTx']/@value").extract()
        fosa['nombre'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[1]/dl/dd[5]/text()').extract()
        fosa['victimas'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[3]/dl/dd[1]/text()').extract()
        fosa['tipo'] = response.xpath('//*[@id="contenido"]/div[2]/div[2]/div[1]/dl/dd/text()').extract()
        fosa['fecha'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[2]/dl/dd[2]/text()').extract()
        fosa['descripcion'] = response.xpath('//*[@id="contenido"]/div[2]/div[1]/div[2]/dl/dd[3]/text()').extract()

        return fosa
