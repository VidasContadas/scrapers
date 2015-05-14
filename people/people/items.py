# -*- coding: utf-8 -*-
import scrapy


class PeopleItem(scrapy.Item):
    name = scrapy.Field()


class VictimaItem(scrapy.Item):
    fosa = scrapy.Field()
    nombre = scrapy.Field()
    apellido = scrapy.Field()
    ciudad = scrapy.Field()
    sexo = scrapy.Field()        
    fecha_muerte = scrapy.Field()

class FosaItem(scrapy.Item):
    nombre = scrapy.Field()
    url = scrapy.Field()
    codigo = scrapy.Field()
    tipo = scrapy.Field()
    comunidad = scrapy.Field()
    provincia = scrapy.Field()
    municipio = scrapy.Field()
    latitud = scrapy.Field()  
    longitud = scrapy.Field()      
    fecha = scrapy.Field()
    titularidad = scrapy.Field()
    foto = scrapy.Field()
    descripcion = scrapy.Field()
    victimas = scrapy.Field()
    relato_historico = scrapy.Field()
    fecha_actuacion = scrapy.Field()
    promotor_actuacion = scrapy.Field()
    descripcion_actuacion = scrapy.Field()
