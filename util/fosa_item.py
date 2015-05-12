from scrapy import Item, Field

class FosaItem(Item):
    url = Field()
    codigo = Field()
    tipo = Field()
    comunidad = Field()
    provincia = Field()
    municipio = Field()
    fecha = Field()
    titularidad = Field()
    foto = Field()
    descripcion = Field()
    victimas = Field()
    relato_historico = Field()
    fecha_actuacion = Field()
    promotor_actuacion = Field()
    descripcion_actuacion = Field()
