import scrapy
from MyProj.items import MyprojItem

class SecondSpider(scrapy.Spider):
    name = "Books2"
    start_urls = ["https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"]

    def parse(self, response):
        item = MyprojItem()
        #item['title'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1').extract()
        #item['price'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]').extract()

        item['title'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()').extract()
        item['price'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()').extract()

        return item