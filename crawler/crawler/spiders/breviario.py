import scrapy
from datetime import date
import locale
from scrapy.http import Request


class BreviarioSpider(scrapy.Spider):
    name = 'breviario_spider'
    start_urls = ['https://rumoasantidade.com.br/livro-breviario-confianca']

    def parse(self, response):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        date_parse = date(2020, int(self.selected_date.split('/')[1]), int(self.selected_date.split('/')[0])).strftime("%-d de %B")
        date_parse = date_parse.replace('janeiro', 'Janeiro').replace('fevereiro', 'Fevereiro').replace('março', 'Março').replace('abril', 'Abril')\
            .replace('maio', 'Maio').replace('junho', 'Junho').replace('julho', 'Julho').replace('agosto', 'Agosto').replace('setembro', 'Setembro')\
            .replace('outubro', 'Outubro').replace('novembro', 'Novembro').replace('dezembro', 'Dezembro')
        url = response.xpath(f"//*[contains(text(), '{date_parse}')]").css('a::attr(href)').get()
        # Chama outra função utilizando o url do dia em questão
        return Request(url=url, callback=self.parse_meditation_of_the_day)

    # scrapy crawl breviario_spider -a selected_date=01/01 -o output.json
    def parse_meditation_of_the_day(self, response):
        return {
            'meditation_day': response.css('h2::text').get(),
            'title': response.css('h1::text').get(),
            'text': ' '.join(response.css('div.pf-content').css('p::text').getall()),
            'reference': response.xpath(f"//*[contains(text(), 'Brandão, Ascânio')]").css('em::text').get()
        }
