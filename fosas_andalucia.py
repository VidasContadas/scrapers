from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from util.fosa_item import FosaItem

class FosasAndaluciaSpider(CrawlSpider):
    name = 'fosasandalucia'
    
    start_urls = [
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=1',
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=2',
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=3',
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=4',
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=5',
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=6',
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=7',
                  'http://www.juntadeandalucia.es/administracionlocalyrelacionesinstitucionales/mapadefosas/busquedaTumbas.cgj?codigoProvincia=8'
                  ]
    
    rules = [Rule(LinkExtractor(allow=['/busquedaTumbas.cgj?\w+']),callback='parse_crave')]

    def parse_crave(self, response):
        fosa = FosaItem()
        fosa['url'] = response.url
        fosa['codigo'] = response.xpath("//div[@class='s_codigo'][1]/text()").extract()[1].strip()
        fosa['tipo'] = response.xpath("//div[@class='s_codigo'][2]/text()").extract()[1].strip()
        
        ubicacion = response.xpath("//div[@class='s_provincia']/text()").extract()
        fosa['comunidad'] = 'Andalucia'
        fosa['provincia'] = ubicacion[1].strip()
        fosa['municipio'] = ubicacion[2].strip()
        
        fecha_titularidad = response.xpath("//div[@class='s_fecha'][1]/text()").extract()
        fosa['fecha'] = fecha_titularidad[1].strip()
        fosa['titularidad'] = fecha_titularidad[2].strip()
        
        foto = response.xpath("//a[@id='fotoFosa']/@href").extract()
        if(len(foto)>0):
            fosa['foto'] = foto[0].strip()
             
        descripcion = response.xpath("//div[@id='s_locades_capa']/div/text()").extract()
        fosa['descripcion'] = '"' + ' '.join(descripcion) + '"'
        
        fosa['victimas'] = response.xpath("//div[@class='s_victimas']/text()").extract()[1].strip()

        relato = response.xpath("//div[@class='s_locades'][2]/following-sibling::div[@class='wtext'][1]/p/text()").extract()
        #fosa['relato_historico'] = '"' + ' '.join(relato) +'"'
        
        fecha_actuacion = response.xpath("//div[@class='s_fecha2'][1]/text()").extract()
        fosa['fecha_actuacion'] = fecha_actuacion[1].strip()
        
        fosa['promotor_actuacion'] = response.xpath("//div[@class='s_promotor'][1]/text()").extract()[1].strip()
        
        descripcion_actuacion = response.xpath("//div[@class='s_locades'][3]/following-sibling::div[@class='wtext'][1]/p/text()").extract()
        fosa['descripcion_actuacion'] = '"' + ' '.join(descripcion_actuacion)+'"'
        
        return fosa
