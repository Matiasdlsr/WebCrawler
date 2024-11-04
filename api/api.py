from flask import Flask, jsonify, request
import json
import os
import subprocess

app = Flask(__name__)

# Ruta a la carpeta donde están myspider.py y summary.py
SPIDER_DIR = os.path.join(os.path.dirname(__file__), '../spider/') 

@app.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    data = request.json
    url = data.get('url')
    print("data {data}")
    print(url)
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # 1. Ejecuta myspider.py con la URL proporcionada
    subprocess.run(['scrapy', 'runspider', os.path.join(SPIDER_DIR, 'myspider.py'), '-a', f'url={url}'])

    # 2. Ejecuta summary.py para procesar los datos generados por myspider.py
    subprocess.run(['python', os.path.join(SPIDER_DIR, 'summary.py')])

    # 3. Carga el archivo summary.json
    summary_path = os.path.join(SPIDER_DIR, 'summary.json')
    try:
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary_data = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'summary.json file not found'}), 500

    # Devuelve el contenido de summary.json
    return jsonify(summary_data)

if __name__ == '__main__':
    app.run(debug=True)
