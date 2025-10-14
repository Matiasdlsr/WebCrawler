from flask import Flask, request, jsonify
import os
import subprocess
import json
import sys
from cache.redis_cache import RedisCache

app = Flask(__name__)
redis_cache = RedisCache()
#direccion de archivos
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
#verificar dominio
    domain = url.split("/")[2]  
    if not any(domain.endswith(allowed_domain) for allowed_domain in ALLOWED_DOMAINS):
        return jsonify({'error': 'Proveedor aun no implementado'}), 400
#obtencion de datos desde cache
    cached_summary = redis_cache.get_cache(url)
    if cached_summary:
        print("Recuperando resumen desde caché.")
        return jsonify(json.loads(cached_summary)), 200
#ejecucacion del script de extracion de datos 'myspider.py'
    try:
        subprocess.run(['scrapy', 'runspider', os.path.join(SPIDER_PATH, 'myspider.py'), '-a', f'url={url}'],
                    check=True, cwd=SPIDER_PATH)
    except subprocess.CalledProcessError as err:
        return jsonify({'error': 'Error al ejecutar el spider'}), 500
#ejecucion del script de resumen de datos 'summary.py'
    try:
        subprocess.run([sys.executable, os.path.join(SPIDER_PATH, 'summary.py')], check=True, cwd=SPIDER_PATH)
#manejo de errores
    except Exception as err:
        return jsonify({"error": "Error al generar el resumen"}), 500
#apertura del archivo 'summary.json'
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r', encoding='utf-8') as file:
            summary_data = json.load(file)
#almacenar datos en cache
        redis_cache.set_cache(url, json.dumps(summary_data))

        return jsonify(summary_data), 200
    else:
        return jsonify({'error': 'No se encontró el archivo de resumen'}), 500

if __name__ == '__main__':
    app.run(debug=True)
