from flask import Flask, request, jsonify
import os
import subprocess
import json


app = Flask(__name__)

SPIDER_PATH = os.path.join(os.path.dirname(__file__), '../spider')
SUMMARY_FILE = os.path.join(SPIDER_PATH, 'summary.json')
VENV_PYTHON = os.path.join(SPIDER_PATH, '../new_env/Scripts/python')

ALLOWED_DOMAINS = ["bbc.com", "clarin.com", "lanacion.com.ar"]


@app.route('/api/summarize', methods=['POST'])
def summarize():
    
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL es requerida'}), 400

    domain = url.split("/")[2]  
    if not any(domain.endswith(allowed_domain) for allowed_domain in ALLOWED_DOMAINS):
        return jsonify({'error': 'Proveedor aun no implementado'}), 400
    
    try:
        subprocess.run(['scrapy', 'runspider', os.path.join(SPIDER_PATH, 'myspider.py'), '-a', f'url={url}'],
                    check=True, cwd=SPIDER_PATH)
    except subprocess.CalledProcessError as err:
        return jsonify({'error': 'Error al ejecutar el spider'}), 500
    
    try:
        subprocess.run([VENV_PYTHON, os.path.join(SPIDER_PATH, 'summary.py')], check=True, cwd=SPIDER_PATH)
    except Exception as err:
        print(f"Error al generar el resumen: {err}")
        return jsonify({"error": "Error al generar el resumen"}), 500

    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r', encoding='utf-8') as file:
            summary_data = json.load(file)
        return jsonify(summary_data), 200
    else:
        return jsonify({'error': 'No se encontró el archivo de resumen'}), 500

if __name__ == '__main__':
    app.run(debug=True)
