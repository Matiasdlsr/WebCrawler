import scrapy
import json

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    start_urls = ['https://www.bbc.com/news/articles/c4g95r3lnr2o']
    
    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        content = response.xpath('//p[not(ancestor::aside)]/text()').getall()
        item = {
            'title' : title,
            'content': " ".join(content)
        }
        
        with open("news.json", "a",encoding='utf-8') as file:
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
    
        yield item
