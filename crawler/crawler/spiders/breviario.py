import scrapy
from datetime import date
import locale
from scrapy.http import Request


class BreviarioSpider(scrapy.Spider):
    name = 'breviario_spider'
    start_urls = ['https://rumoasantidade.com.br/livro-breviario-confianca']

    def parse(self, response):
        locale.setlocale(locale.LC_TIME, "pt_BR")
        date_parse = date(2020, self.selected_date.split('/')[1], self.selected_date.split('/')[0]).strftime(
            "%-d de %B")
        url = response.xpath(f"//*[contains(text(), '{date_parse}')]").css('a::attr(href)').get()
        # Chama outra função utilizando o url do dia em questão
        yield Request(url=url, callback=self.parse_page)

    # Como fazer crawl nesta página?
    def parse_page(self, response):
        yield {
            'text': ' '.join(response.css('div.pf-content').css('p::text').getall()),
            'reference': ' '.join(response.css('div.pf-content').css('p::text').getall())
        }
