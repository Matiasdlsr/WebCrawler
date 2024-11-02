
# ?
import json
class JsonWriterPipeline:
    def open_spider (self,spider):
        self.file = open ('salida_output.json', "w")
        self.file.write('[')
        self.first_item = True
    
    def close_spider(self,spider):
        self.file.write (']')
        self.file.close ()
        
    def process_item (self,item,spider):
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        line = json.dumps(dict(item))
        self.item.write(line)
        return item