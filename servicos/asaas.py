import os
import requests
from dotenv import load_dotenv

load_dotenv()
ASAAS_API_KEY = os.getenv("ASAAS_API_KEY")
URL_BASE = "https://api.asaas.com/v3"
HEADERS = {"access_token": ASAAS_API_KEY, "Content-Type": "application/json"}


def criar_cliente_asaas(nome, cpf):
    payload = {"name": nome, "cpfCnpj": cpf}
    resposta = requests.post(f"{URL_BASE}/customers", json=payload, headers=HEADERS)
    if resposta.status_code != 200:
        raise Exception(f"Erro Asaas (Cliente): {resposta.text}")
    return resposta.json().get('id')


def criar_assinatura_pix(cliente_id, valor):
    if not cliente_id:
        raise Exception("Cliente ID inválido.")

    payload = {
        "customer": cliente_id,
        "billingType": "PIX",
        "value": valor,
        "cycle": "MONTHLY",
        "description": "Mensalidade Sócio - Sport Club Genus"
    }
    resposta = requests.post(f"{URL_BASE}/subscriptions", json=payload, headers=HEADERS)
    if resposta.status_code != 200:
        raise Exception(f"Erro Asaas (Assinatura): {resposta.text}")
    return resposta.json()