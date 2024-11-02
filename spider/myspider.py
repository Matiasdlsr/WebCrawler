


import scrapy

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    start_urls = ['https://www.bbc.com/news/articles/c4g95r3lnr2o']
    
    def parse(self, response):
        title = response.xpath ('//div[@class="sc-18fde0d6-0 eeiVGB"]/h1/text()').get()
        content = response.xpath('//div[@class="sc-18fde0d6-0 dlWCEZ"]/p/text()').getall()
        item = {
            'title' : title,
            'content': content
        }
        
        yield item
