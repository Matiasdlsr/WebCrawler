


import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    start_urls = ['https://www.bbc.com/news/articles/c4g95r3lnr2o']
    
    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        content = response.xpath('//p/text()').getall()
        item = {
            'title' : title,
            # 'content': content
            'content': " ".join(content) #combina todo el contenido en una sola cadena de texto
        }
        

        yield item
