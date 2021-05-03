import scrapy
from scrapy.http import Request

class BreviarioSpider(scrapy.Spider):
    name = 'breviario_spider'
    start_urls = ['https://rumoasantidade.com.br/livro-breviario-confianca']

    def parse(self, response):
        url = response.xpath("//*[contains(text(), '2 de Janeiro')]").css('a::attr(href)').get()
        # Chama outra função utilizando o url do dia em questão
        yield Request(url=url, callback=self.parse_page)

    # Como fazer crawl nesta página?
    def parse_page(self, response):
        text = ' '.join(response.css('div.pf-content').css('p::text').getall())
        return text



