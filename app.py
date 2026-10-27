import os
import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify, render_template
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
# from rotas.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(adesao_bp)
# app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)