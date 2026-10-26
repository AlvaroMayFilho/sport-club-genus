from firebase_admin import firestore


@firestore.transactional
def travar_limite_cotas(transaction, db, grupo_id, user_id, dados_socio):
    grupo_ref = db.collection('grupos').document(grupo_id)
    grupo_snapshot = grupo_ref.get(transaction=transaction)

    if not grupo_snapshot.exists:
        raise ValueError("Grupo não encontrado no banco de dados.")

    grupo_dados = grupo_snapshot.to_dict()

    # Validação do Hard Cap de cotas
    if grupo_dados['cotas_vendidas'] >= grupo_dados['max_cotas']:
        raise Exception(f"Limite máximo de {grupo_dados['max_cotas']} cotas atingido.")

    nova_cota = grupo_dados['cotas_vendidas'] + 1

    # Executa a trava incrementando o contador na coleção de grupos
    transaction.update(grupo_ref, {
        'cotas_vendidas': nova_cota
    })

    # Registra o sócio na coleção individual com o número exato da cota
    socio_ref = db.collection('socios').document(user_id)
    dados_socio['numero_cota'] = nova_cota
    transaction.set(socio_ref, dados_socio)

    return nova_cota