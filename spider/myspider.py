import scrapy # type: ignore
import json
import os

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    #Definir URL y archivo json de salida
    def __init__(self, url=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.output_file = os.path.join("..", "api", "data", "news.json")  
#Parsear datos 
    def parse(self, response):
        try:
            title, content = self.extract_data(response)
            
            if not title or not content:
                self.logger.warning("Titulo o contenido no encontrado")
                return
#crear estructura item
            item = {
                'url': response.url,
                'title': self.clean_text(title),
                'content': self.clean_text(" ".join(content))
            }

            self.save_to_file(item) 
            yield item
        except Exception as e:
            self.logger.error(f"Error al parsear: {e}")
#Extracion de titulo y contenido
    def extract_data(self, response):
        title = response.xpath('//h1/text()').get()
        content = response.xpath('//p[not(ancestor::aside)]/text()').getall()
        return title, content

    def clean_text(self, text):
        return " ".join(text.split())
    
#Guardar contenido en el archivo json
    def save_to_file(self, item):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        try:
            with open(self.output_file, "w", encoding='utf-8') as file:
                json.dump(item, file, ensure_ascii=False, indent=4)  
        
        except Exception as e:
            self.logger.error(f"Error guardando en el archivo: {e}")
