import scrapy
from datetime import date
import locale
from scrapy.http import Request


class BreviarioSpider(scrapy.Spider):
    name = 'breviario_spider'
    start_urls = ['https://rumoasantidade.com.br/livro-breviario-confianca']

    def parse(self, response):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        # Transforma a data recebida por parâmetro para o formato "Dia de mês"
        date_parse = date(2020, int(self.selected_date.split('/')[1]), int(self.selected_date.split('/')[0])).strftime("%-d de %B")
        # Substitui caracteres minúsculos iniciais de meses por maiúsculos para o crawling funcionar.
        # TODO buscar solução mais elegante
        date_parse = date_parse.replace('janeiro', 'Janeiro').replace('fevereiro', 'Fevereiro').replace('março', 'Março').replace('abril', 'Abril')\
            .replace('maio', 'Maio').replace('junho', 'Junho').replace('julho', 'Julho').replace('agosto', 'Agosto').replace('setembro', 'Setembro')\
            .replace('outubro', 'Outubro').replace('novembro', 'Novembro').replace('dezembro', 'Dezembro')

        # Busca endereço para a meditação do dia, que fica em um link após a data por extenso
        url = response.xpath(f"//*[contains(text(), '{date_parse}')]").css('a::attr(href)').get()

        # Chama outra função utilizando o url da meditação do dia em questão
        return Request(url=url, callback=self.parse_meditation_of_the_day)

    # Extrai texto da meditação do dia e retorna
    def parse_meditation_of_the_day(self, response):
        text_array = response.xpath('//div[@class="pf-content"]/descendant::text()').extract()
        text_array[0] = ''
        text_array[1] = ''
        text_array[len(text_array) - 1] = ''
        text_array[len(text_array) - 2] = ''
        text_array[len(text_array) - 3] = ''
        return {
            'meditation_day': response.css('h2::text').get(),
            'title': response.css('h1::text').get(),
            'text': ' '.join(text_array),
            'reference': response.xpath(f"//*[contains(text(), 'Brandão, Ascânio')]").css('em::text').get()
        }
