import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify
from flask import Flask, jsonify, render_template

# 1. Inicializa o Firebase PRIMEIRO
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)

# 2. Somente AGORA importa as rotas que dependem do banco
from rotas.adesao import adesao_bp

# 3. Cria e configura o app Flask
app = Flask(__name__)
app.register_blueprint(adesao_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)