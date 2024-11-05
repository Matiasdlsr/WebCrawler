import scrapy
import json
import time
import os

class NewsSpider(scrapy.Spider):
    name = "news_spider"

    def __init__(self, url=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.timestamp = str(int(time.time()))
        self.output_file = os.path.join("..", "api", "data", f"news_{self.timestamp}.json")

    def parse(self, response):
        try:
            title, content = self.extract_data(response)
            
            if not title or not content:
                self.logger.warning("Title or content not found.")
                return

            item = {
                'url': response.url,
                'title': self.clean_text(title),
                'content': self.clean_text(" ".join(content))
            }

            self.save_to_file(item)
            yield item
        except Exception as e:
            self.logger.error(f"Error in parsing: {e}")

    def extract_data(self, response):
        title = response.xpath('//h1/text()').get()
        content = response.xpath('//p[not(ancestor::aside)]/text()').getall()
        return title, content

    def clean_text(self, text):
        return " ".join(text.split())

    def save_to_file(self, item):
        os.makedirs("./api/data", exist_ok=True)
        try:
            with open(self.output_file, "w", encoding='utf-8') as file:
                json.dump(item, file, ensure_ascii=False, indent=4)
        except Exception as e:
            self.logger.error(f"Error saving item to file: {e}")
