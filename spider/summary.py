import json
import re
import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Ruta específica para encontrar `news.json` en `api/data`
NEWS_DIR = os.path.join(os.path.dirname(__file__), '../api/data')
SUMMARY_PATH = os.path.join(os.path.dirname(__file__), 'summary.json')

def get_latest_news_file(directory=NEWS_DIR):
    # Filtra y selecciona el archivo más reciente que coincida con el patrón "news_*.json"
    files = [f for f in os.listdir(directory) if f.startswith("news_") and f.endswith(".json")]
    if not files:
        raise FileNotFoundError("No se encontró ningún archivo de noticias para procesar.")
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(directory, f)))
    print(f"Archivos encontrados en {NEWS_DIR}: {files}")
    print(f"Último archivo detectado: {latest_file}")
    return os.path.join(directory, latest_file)

def summarize_content(input_filename, output_filename=SUMMARY_PATH):
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    summaries = []
    if isinstance(data, dict):
        title = data.get('title')
        content = " ".join(data.get('content', []))

        if content.strip():
            parser = PlaintextParser.from_string(content, Tokenizer("english"))
            summarizer = LexRankSummarizer()
            summary = summarizer(parser.document, 5)

            summary_text = " ".join(str(sentence) for sentence in summary)
            summary_text = re.sub(r'(?<=\w) (?=\w)', '', summary_text)
            summary_text = re.sub(r' {3,}', ' ', summary_text)
            summaries.append({"title": title, "summary": summary_text})

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(summaries, outfile, ensure_ascii=False, indent=4)
        print(f"Resumen guardado en {output_filename}")

# Ejecutar el resumen sobre el archivo de noticias más reciente en `NEWS_DIR`
try:
    latest_news_file = get_latest_news_file()
    summarize_content(latest_news_file)
    print(f"Resumen generado en summary.json basado en {latest_news_file}")
except FileNotFoundError as e:
    print(e)
