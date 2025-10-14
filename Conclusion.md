Despues de una investigacion del mejor lenguaje y herramientas para hacer web crawler, llegue a la conclusion de usar Python con: 

Scrapy: Una de las librerias mas populares para crear webs crawlers para la extraccion del titulo y contenido principal de articulos de noticias 

NLTK: Libreria para procesamiento de lenguaje natural // Sumy: Libreria para resumen automatico de texto (parece que sumy utiliza nltk)

Flask: Para la creacion de API RESTful 

Redis para guardar en cache los resumenes generados y poder acceder rapidamente a estos.

Json: como formato de salida para los resumenes

Updates:

-Optimizacion de rendimiento con Multiprocessing o Asyncio

-Manejo de errores

Estadisticas -> El resumen generado actualmente resume el contenido ~30%


## Pasos para iniciar el proyecto

Instalar dependencias: pip install -r requirements.txt

Descargar el servidor de redis: https://github.com/MicrosoftArchive/redis/releases

Iniciar el servidor de redis: redis-server

<!-- Instalar twisted : pip install twisted==22.10.0 -->

en \lib\sumy\models\tf.py cambiar from collections import Sequence por from collections.abc import Sequence

fijarse el archivo download_nltk y su contenido punk o punk_tab


Ejecutar la API : python -m api.api

Realizar la peticion (en gitbash): 

curl -X POST http://127.0.0.1:5000/api/summarize -H "Content-Type: application/json" -d "{\"url\": \"https://www.bbc.com/mundo/articles/c981zn3ymygo\"}"

curl -X POST http://127.0.0.1:5000/api/summarize -H "Content-Type: application/json" -d "{\"url\": \"https://www.lanacion.com.ar/deportes/automovilismo/la-discusion-de-franco-colapinto-con-su-equipo-cuando-pidio-entrar-a-boxes-para-cambiar-los-nid03112024/\"}"

curl -X POST http://127.0.0.1:5000/api/summarize -H "Content-Type: application/json" -d "{\"url\": \"https://www.infobae.com/deportes/2024/11/01/franco-colapinto-con-infobae-su-futuro-los-elogios-de-hamilton-y-verstappen-y-el-furor-de-los-hinchas-argentinos/\"}"