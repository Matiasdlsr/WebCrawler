import json
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def summarize_content(input_filename, output_filename):
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

summarize_content('news.json', 'summary.json')

