import scrapy

class BreviarioSpider(scrapy.Spider):
    name = 'breviario_spider'
    start_urls = ['https://rumoasantidade.com.br/livro-breviario-confianca']

    def parse(self, response):
        url = response.xpath("//*[contains(text(), '2 de Janeiro')]").css('a::attr(href)').get()
        print(url)




