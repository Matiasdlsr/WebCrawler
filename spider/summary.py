import json
import os
import logging
from sumy.parsers.plaintext import PlaintextParser # type: ignore
from sumy.nlp.tokenizers import Tokenizer # type: ignore
from sumy.summarizers.lex_rank import LexRankSummarizer # type: ignore


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


NEWS_DIR = os.path.join(os.path.dirname(__file__), '../api/data')
SUMMARY_PATH = os.path.join(os.path.dirname(__file__), 'summary.json')

def get_latest_news_file(directory=NEWS_DIR):
    files = [file for file in os.listdir(directory) if file.startswith("news") and file.endswith(".json")]
    if not files:
        raise FileNotFoundError("No se encontró ningún archivo de noticias para procesar.")
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(directory, f)))
    logger.info(f"Último archivo detectado: {latest_file}")
    return os.path.join(directory, latest_file)


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

    if not content.strip():
        logger.warning("El contenido está vacío, no se generará el resumen.")
        return

    parser = PlaintextParser.from_string(content, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentence_count)
    summary_text = " ".join(str(sentence) for sentence in summary)
    

    summary_data = [{"title": title, "summary": summary_text}]
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(summary_data, outfile, ensure_ascii=False, indent=4)
        logger.info(f"Resumen guardado en {output_filename}")
    except IOError as err:
        logger.error(f"Error al guardar el resumen: {err}")

try:
    latest_news_file = get_latest_news_file()
    summarize_content(latest_news_file)
    logger.info(f"Resumen generado en summary.json basado en {latest_news_file}")
except FileNotFoundError as err:
    logger.error(err)
