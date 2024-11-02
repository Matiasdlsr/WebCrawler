#?
REQUEST_FINDERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsincioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8" #codificacion de la exportacion 
ITEM_PIPELINES={
    'spider.pipelines.JsonWriterPipeline' : 300, #activacion de propiedad para guardar json
}