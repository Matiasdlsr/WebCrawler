Despues de una investigacion del mejor lenguaje y herramientas para hacer web crawler, llegue a la conclusion de usar Python con: 

Scrapy: Una de las librerias mas populares para crear webs crawlers para la extraccion del titulo y contenido principal de articulos de noticias 

NLTK: Libreria para procesamiento de lenguaje natural // Sumy: Libreria para resumen automatico de texto (parece que sumy utiliza nltk)

Flask: Para la creacion de API RESTful 

Redis // SQL Server // SQLite ??

Json: como formato de salida para los resumenes

Updates:

-Optimizacion de rendimiento con Multiprocessing o Asyncio

-Manejo de errores

Estadisticas (2/11) -> El resumen generado actualmente resume el contenido ~30%

Mejoras (2/11) -> El procesamiento de texto no toma palabras resaltadas, hipervinculos.

Problemas (2/11) -> El resumen genera espacios entre cada letra y palabra (solucionado con expresiones regulares)