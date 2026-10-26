from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from servicos.travas import travar_limite_cotas
from servicos.asaas import criar_cliente_asaas, criar_assinatura_pix

adesao_bp = Blueprint('adesao', __name__)
db = firestore.client()


@adesao_bp.route('/api/adesao/torcedor', methods=['POST'])
def adesao_torcedor():
    dados = request.json
    user_id = dados.get('user_id')
    grupo_id = dados.get('grupo_id')
    nome = dados.get('nome')
    cpf = dados.get('cpf')

    transaction = db.transaction()
    try:
        dados_socio = {
            'grupo_id': grupo_id,
            'status_adimplencia': 'PENDENTE',
            'parcelas_pagas': 0
        }
        numero_cota = travar_limite_cotas(transaction, db, grupo_id, user_id, dados_socio)

        # Criação no Asaas (usando 20.00 fixo para teste do Bronze)
        cliente_id = criar_cliente_asaas(nome, cpf)
        assinatura = criar_assinatura_pix(cliente_id, 20.00)

        return jsonify({
            "status": "sucesso",
            "cota": numero_cota,
            "assinatura_id": assinatura.get('id')
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400