import scrapy
import json
import time
import os

class NewsSpider(scrapy.Spider):
    name = "news_spider"

    def __init__(self, url=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.timestamp = str(int(time.time()))  # Agrega un timestamp único
        self.output_file = f"data/news_{self.timestamp}.json"

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        content = response.xpath('//p[not(ancestor::aside)]/text()').getall()

        item = {
            'url': response.url,
            'title': title,
            'content': " ".join(content)
        }

        # Crear el directorio si no existe
        os.makedirs("data", exist_ok=True)
        
        with open(self.output_file, "w", encoding='utf-8') as file:
            json.dump(item, file, ensure_ascii=False, indent=4)

        yield item
