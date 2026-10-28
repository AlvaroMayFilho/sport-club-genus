import os
import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Define o caminho absoluto da pasta raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Força a leitura do .env usando o caminho absoluto
load_dotenv(os.path.join(BASE_DIR, '.env'))

if not firebase_admin._apps:
    # Lê a variável ou usa o caminho absoluto do json como fallback
    caminho_firebase = os.getenv("FIREBASE_CREDENTIALS_PATH", os.path.join(BASE_DIR, "firebase-key.json"))
    cred = credentials.Certificate(caminho_firebase)
    firebase_admin.initialize_app(cred)

from rotas.adesao import adesao_bp

app = Flask(__name__)

# Proteção CORS para permitir apenas o domínio oficial e o localhost
CORS(app, resources={r"/api/*": {"origins": ["https://scgenus.com.br", "https://www.scgenus.com.br", "http://127.0.0.1:5000"]}})

app.register_blueprint(adesao_bp)

# 1. Rota Frontend (Entrega a página HTML)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Rota Backend API (Entrega os dados em JSON)
@app.route('/api/jogos', methods=['GET'])
def obter_jogos():
    jogos = [
        { "campeonato": "Campeonato Rondoniense 2026", "mandante": "GENUS", "visitante": "JI-PARANÁ", "data": "15/02/2026", "hora": "16:00", "local": "Aluizão - Porto Velho, RO" },
        { "campeonato": "Campeonato Rondoniense 2026", "mandante": "VILHENA", "visitante": "GENUS", "data": "22/02/2026", "hora": "19:00", "local": "Portal da Amazônia - Vilhena, RO" },
        { "campeonato": "Copa do Brasil 2026", "mandante": "GENUS", "visitante": "REMO", "data": "05/03/2026", "hora": "20:30", "local": "Aluizão - Porto Velho, RO" }
    ]
    return jsonify(jogos)

if __name__ == '__main__':
    app.run(debug=True)