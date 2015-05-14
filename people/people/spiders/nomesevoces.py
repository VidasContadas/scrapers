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

class NomesSpider(CrawlSpider):
    name = 'nomesevoces'
    allowed_domains = ['vitimas.nomesevoces.net', ]

    start_urls = [
            'http://vitimas.nomesevoces.net/gl/buscar/?pax=1', ]

    ofile  = open('nomesevoces.csv', "wb")
    writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)  

    cabecera = ["URL","Nombre","Sexo", "Edad", "Profesion", "Natural de", "Vecino de","Tipo","Suceso","Fecha de muerte"]

    writer.writerow(cabecera)

    def location_href_value(value):
        m = re.search("location.href=\'(.*)\'", value)
        return m.groups()[0]

    rules = [
        Rule(SgmlLinkExtractor(
            allow=['/gl/buscar/\?pax=\d+'], unique=True), follow=True),
        Rule(SgmlLinkExtractor(
            allow=['/gl/ficha/\d+/'], unique=True), 'parse_item'),]
      
    def parse_item(self, response):

        data=re.sub('<br>',' ',response.body)

        html = BeautifulSoup(data)

        t1 = html.findAll('p', {'class':'t1'})

        #fields

        name = ''
        genre_html = ''
        edad = ''
        profesion = ''
        tipo = ''
        suceso = ''
        fecha_muerte = ''
        natural = ''
        vecindad = ''

        name = html.h2.text
        tipo = html.p.a.text

        m = re.search('de (\d+) anos',t1[0].text)
        if m:
            edad = m.group(1)

        m = re.search('Morto o (.*)',t1[0].text)
        if m:
            fecha_muerte = m.group(1)

        for a in t1[0].findAll('a'):
            if "sexo" in a.attrs['href']:
                genre_html = a.text
            if "profesion" in a.attrs['href']:
                profesion = a.text
            if "vecinanza" in a.attrs['href']:
                vecindad = a.text
            if "natural" in a.attrs['href']:
                natural = a.text

        suceso = t1[1].text.strip(' \n\t')

        item = items.PeopleItem()
        item['url'] = response.url

        #name
        item['name'] = name

        #genre
        item['genre'] = 'F' if genre_html == 'Muller'\
                        else 'M' if genre_html == 'Home'\
                        else 'U'

        row = []
        row.append(response.url)
        row.append(name.encode("utf-8"))
        row.append(genre_html)        
        row.append(edad)
        row.append(profesion.encode("utf-8"))
        row.append(natural.encode("utf-8"))
        row.append(vecindad.encode("utf-8"))
        row.append(tipo.encode("utf-8"))
        row.append(suceso.encode("utf-8"))
        row.append(fecha_muerte.encode("utf-8"))

        print name
        self.writer.writerow(row)

        return item

