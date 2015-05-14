# coding=utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import scrap.items as items
from common.models import CustomDate

from bs4 import BeautifulSoup

import re
import csv

def get_int_from_text(expression, sub, text):
    re_result = re.search(expression, text, re.M|re.I|re.U)
    return int(re.sub(sub, '', re_result.group())) if re_result else 0

def extract_text(expression, text):
    re_result = re.search(expression, text, re.M|re.I|re.U)
    return re_result.groups()[0] if re_result else ""

class UnavarraSpider(CrawlSpider):
    name = 'unavarra'
    allowed_domains = ['memoria-oroimena.unavarra.es', ]

    start_urls = [
            'http://memoria-oroimena.unavarra.es/es/buscar/?pax=1', ]

    ofile  = open('ttest.csv', "wb")
    writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)  

    cabecera = ["URL","Nombre","Sexo","Edad",
        "Profesión","Cargo","Filiación","Partido/Sindicato",
        "Fecha nacimiento - Año","Fecha nacimiento - Mes","Fecha nacimiento - Día",
        "Fecha muerte","Fecha muerte - Año","Fecha muerte - Mes","Fecha muerte - Día",
        "Nacimiento - Concejo o barrio", "Nacimiento - Municipio", "Nacimiento - Comarca", "Nacimiento - Provincia",
        "Vecindad - Concejo o barrio", "Vecindad - Municipio", "Vecindad - Comarca", "Vecindad - Provincia",
        "Muerte - Concejo o barrio", "Muerte - Municipio", "Muerte - Comarca", "Muerte - Provincia",
        ]

    writer.writerow(cabecera)

    def location_href_value(value):
        m = re.search("location.href=\'(.*)\'", value)
        return m.groups()[0]

    rules = [
        Rule(SgmlLinkExtractor(
            allow=['/es/buscar/\?pax=\d+'], unique=True), follow=True),
        Rule(SgmlLinkExtractor(
            allow=['.*'], tags=('div'), attrs=('onclick'), unique=True,
            process_value=location_href_value), 'parse_item'),]
      
    def parse_item(self, response):

        data=re.sub('<br>',' ',response.body)

        html = BeautifulSoup(data)

        ficha = html.find('div', {'class':'ficha_desc'})

        #fields

        name = ficha.find('h2').text
        genre_html = ficha.find('p', 't1').next_element
        birth_year=get_int_from_text(u'A\xf1o: \d{4}','A\xf1o: ',ficha.text)
        birth_month=get_int_from_text(u'Mes: \d{1,2}','Mes: ',ficha.text)
        birth_day=get_int_from_text(u'D\xeda: \d{1,2}','D\xeda: ',ficha.text)
        age = get_int_from_text(u'Edad: \d{1,3}','Edad: ',ficha.text)
        
        lugar_nac = re.search(ur'Concejo o barrio: (.*?) Municipio: (.*?) Comarca: (.*?) Provincia: (.*) Vecindad',ficha.text, re.M|re.I|re.U)

        concejo_o_barrio_nac = lugar_nac.groups()[0]
        municipio_nac = lugar_nac.groups()[1]
        comarca_nac = lugar_nac.groups()[2]
        provincia_nac = lugar_nac.groups()[3]

        vecindad = re.search(ur'Vecindad  Concejo o barrio: (.*?) Municipio: (.*?) Comarca: (.*?) Provincia: (.*) Profesi\xf3n/Filiaci\xf3n/Cargo/Partido',ficha.text, re.M|re.I|re.U)

        concejo_o_barrio_vec = vecindad.groups()[0]
        municipio_vec = vecindad.groups()[1]
        comarca_vec = vecindad.groups()[2]
        provincia_vec = vecindad.groups()[3]

        politica = re.findall(u'Profesión: (.*?) Ocupó el cargo de: (.*?) Filiación sociopolítica: (.*?) Partido/Sindicato: (.*?) ',ficha.text, re.M|re.I|re.U)
        profesion = politica[0][0]
        cargo = politica[0][1]
        filiacion = politica[0][2]
        partido = politica[0][3]

        ficha2 = html.find('div', {'class':'ficha_desc_derecha'})

        death_year=get_int_from_text(u'A\xf1o: \d{4}','A\xf1o: ',ficha2.text)
        death_month=get_int_from_text(u'Mes: \d{1,2}','Mes: ',ficha2.text)
        death_day=get_int_from_text(u'D\xeda: \d{1,2}','D\xeda: ',ficha2.text)

        fecha_muerte = "%s/%s/%s" % (death_day,death_month,death_year)

        lugar_muerte = re.search(ur'Lugar de muerte  Concejo o barrio: (.*?) Municipio: (.*?) Comarca: (.*?) Provincia: (.*) Inform',ficha2.text, re.M|re.I|re.U)

        concejo_o_barrio_muerte = lugar_muerte.groups()[0]
        municipio_muerte = lugar_muerte.groups()[1]
        comarca_muerte = lugar_muerte.groups()[2]
        provincia_muerte = lugar_muerte.groups()[3]

        info_muerte = re.search( r'Informaci\xf3n de muerte/Exhumaci\xf3n  Localizaci\xf3n de muerte: (.*) Hora de muerte: (.*) Causa de muerte: (.*) Informe de muerte: (.*) Enterramiento: (.*)', ficha2.text.replace('\n',' '), re.M|re.I|re.U)

        item = items.PeopleItem()
        item['url'] = response.url

        #name
        item['name'] = name

        #genre
        item['genre'] = 'F' if genre_html == 'Mujer'\
                        else 'M' if genre_html == 'Hombre'\
                        else 'U'

        #birth date
        date_birth, created = CustomDate.objects.get_or_create(
                 year=get_int_from_text(u'A\xf1o: \d{4}','A\xf1o: ',ficha.text),
                 month=get_int_from_text(u'Mes: \d{1,2}','Mes: ',ficha.text),
                 day=get_int_from_text(u'D\xeda: \d{1,2}','D\xeda: ',ficha.text))
        #date_birth.save()
        #item['date_birth'] = date_birth

        #Age
        item['age'] = age

        # import ipdb
        # ipdb.set_trace()

        # item.save()

        row = []
        row.append(response.url)
        row.append(name.encode("utf-8"))
        row.append(genre_html)        
        row.append(age)
        row.append(profesion.encode("utf-8"))
        row.append(cargo.encode("utf-8"))
        row.append(filiacion.encode("utf-8"))
        row.append(partido.encode("utf-8"))
        row.append(birth_year)
        row.append(birth_month)
        row.append(birth_day)
        row.append(fecha_muerte)
        row.append(death_year)
        row.append(death_month)
        row.append(death_day)        
        row.append(concejo_o_barrio_nac.encode("utf-8"))
        row.append(municipio_nac.encode("utf-8"))
        row.append(comarca_nac.encode("utf-8"))
        row.append(provincia_nac.encode("utf-8"))
        row.append(concejo_o_barrio_vec.encode("utf-8"))
        row.append(municipio_vec.encode("utf-8"))
        row.append(comarca_vec.encode("utf-8"))
        row.append(provincia_vec.encode("utf-8"))
        row.append(concejo_o_barrio_muerte.encode("utf-8"))
        row.append(municipio_muerte.encode("utf-8"))
        row.append(comarca_muerte.encode("utf-8"))
        row.append(provincia_muerte.encode("utf-8"))

        print name
        self.writer.writerow(row)

        return item

