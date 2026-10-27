import os
import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

# Carrega as variáveis do .env local (no servidor, as variáveis do painel têm prioridade)
load_dotenv()

if not firebase_admin._apps:
    # Lê o caminho da nuvem, ou usa o local por padrão
    caminho_firebase = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-key.json")
    cred = credentials.Certificate(caminho_firebase)
    firebase_admin.initialize_app(cred)

from rotas.adesao import adesao_bp


app = Flask(__name__)
app.register_blueprint(adesao_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)