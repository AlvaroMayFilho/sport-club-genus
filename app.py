import os
import time
import firebase_admin
from firebase_admin import credentials, firestore
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

# Cliente do Firestore (usado nas rotas de leitura de vagas)
db = firestore.client()

from rotas.adesao import adesao_bp

app = Flask(__name__)

# Proteção CORS para permitir apenas o domínio oficial e o localhost
CORS(app, resources={r"/api/*": {"origins": ["https://scgenus.com.br", "https://www.scgenus.com.br", "http://127.0.0.1:5000"]}})

app.register_blueprint(adesao_bp)

# 1. Rota Frontend (Entrega a página HTML)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planos')
def planos():
    return render_template('planos.html')

# NOVA ROTA: Loja Oficial
@app.route('/loja')
def loja():
    return render_template('loja.html')

# 2. Rota Backend API (Entrega os dados em JSON)
@app.route('/api/jogos', methods=['GET'])
def obter_jogos():
    jogos = [
        { "campeonato": "Campeonato Rondoniense 2026", "mandante": "GENUS", "visitante": "JI-PARANÁ", "data": "15/02/2026", "hora": "16:00", "local": "Aluizão - Porto Velho, RO" },
        { "campeonato": "Campeonato Rondoniense 2026", "mandante": "VILHENA", "visitante": "GENUS", "data": "22/02/2026", "hora": "19:00", "local": "Portal da Amazônia - Vilhena, RO" },
        { "campeonato": "Copa do Brasil 2026", "mandante": "GENUS", "visitante": "REMO", "data": "05/03/2026", "hora": "20:30", "local": "Aluizão - Porto Velho, RO" }
    ]
    return jsonify(jogos)

# 3. Vagas reais (Firestore: coleções "grupos" e "investidor")
CACHE_VAGAS_SEGUNDOS = 30
_cache_vagas = {"ts": 0, "dados": None}


def _montar_vaga(doc_dict):
    """Normaliza um documento do Firestore para o formato que o front usa."""
    vendidas = int(doc_dict.get("cotas_vendidas", 0) or 0)
    maximo = int(doc_dict.get("max_cotas", 0) or 0)
    restantes = max(maximo - vendidas, 0)
    percentual = round(min(vendidas / maximo * 100, 100), 1) if maximo > 0 else 0
    return {
        "nome_plano": doc_dict.get("nome_plano"),
        "valor_mensal": doc_dict.get("valor_mensal"),
        "cotas_vendidas": vendidas,
        "max_cotas": maximo,
        "restantes": restantes,
        "percentual": percentual,
    }


def _ler_vagas_firestore():
    grupos = {}
    for doc in db.collection("grupos").stream():
        grupos[doc.id] = _montar_vaga(doc.to_dict() or {})

    investidor = None
    doc_inv = db.collection("investidor").document("Investidor").get()
    if doc_inv.exists:
        investidor = _montar_vaga(doc_inv.to_dict() or {})

    return {"grupos": grupos, "investidor": investidor}


@app.route('/api/vagas', methods=['GET'])
def obter_vagas():
    agora = time.time()

    # Cache curto em memória para não ler o Firestore a cada visita
    if _cache_vagas["dados"] is not None and agora - _cache_vagas["ts"] < CACHE_VAGAS_SEGUNDOS:
        return jsonify(_cache_vagas["dados"])

    try:
        dados = _ler_vagas_firestore()
    except Exception as erro:
        app.logger.error("Erro ao ler vagas no Firestore: %s", erro)
        return jsonify({"erro": "Não foi possível carregar as vagas agora."}), 503

    _cache_vagas["dados"] = dados
    _cache_vagas["ts"] = agora
    return jsonify(dados)


if __name__ == '__main__':
    app.run(debug=True)