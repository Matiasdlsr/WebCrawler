import json
import os
import logging
from sumy.parsers.plaintext import PlaintextParser # type: ignore
from sumy.nlp.tokenizers import Tokenizer # type: ignore
from sumy.summarizers.lex_rank import LexRankSummarizer # type: ignore

#log de: informacion y errores
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Direcciones de archivos 
NEWS_DIR = os.path.join(os.path.dirname(__file__), '../api/data')
SUMMARY_PATH = os.path.join(os.path.dirname(__file__), 'summary.json')

def get_news_file(directory=NEWS_DIR, filename="news.json"):
    # Ruta completa del archivo news.json en el directorio especificado
    news_file_path = os.path.join(directory, filename)
    
    # Verifica si el archivo existe si no, lanza un error
    if not os.path.exists(news_file_path):
        raise FileNotFoundError("No se encontró el archivo de noticias 'news.json' para procesar.")
    logger.info(f"Archivo de noticias detectado: {news_file_path}")
    return news_file_path

#apertura de archivo 'news.json'
def summarize_content(input_filename, output_filename=SUMMARY_PATH, sentence_count=5):
    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as err:
        logger.error(f"Error al decodificar JSON: {err}")
        return

    title = data.get('title', "Sin título")
    content = data.get('content', "")
    if isinstance(content, list):
        content = " ".join(content)
#deteccion de contenido vacio
    if not content.strip():
        logger.warning("El contenido está vacío, no se generará el resumen.")
        return
#parsear contenido 
    parser = PlaintextParser.from_string(content, Tokenizer("spanish"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    summary_text = " ".join(str(sentence) for sentence in summary)
    

    summary_data = [{"title": title, "summary": summary_text}]
    #guarda el resumen en summary.json
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(summary_data, outfile, ensure_ascii=False, indent=4)
        logger.info(f"Resumen guardado en {output_filename}")
    except IOError as err:
        logger.error(f"Error al guardar el resumen: {err}")

    # Obtiene la ruta de 'news.json' y genera el resumen
try:
    news_file = get_news_file()
    summarize_content(news_file)
    logger.info(f"Resumen generado en summary.json basado en {news_file}")
except FileNotFoundError as err:
    logger.error(err)
