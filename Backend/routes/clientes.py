from backend import app
from flask import render_template, request, jsonify
from Database.models import *

@app.route('/get_leads', methods=['GET'])
def get_leads():
    leads = session.query(cliente).all()
    return jsonify([{'id': lead.id, 'nome': lead.nome, 'email': lead.email, 'telefone': lead.telefone, 'cidade_UF': lead.cidade_UF} for lead in leads])

@app.route('/novo_lead', methods=['POST'])
def novo_lead(dados):
    if not dados:
        return {'error': 'Dados do cliente não fornecidos'}, 400

    cliente_obj = cliente(
        nome=dados.get('nome'),
        cpf=dados.get('cpf'),
        email=dados.get('email'),
        telefone=dados.get('telefone'),
        cidade_UF=dados.get('cidade_UF')
    )
    
    session.add(cliente_obj)
    session.commit()

    return f"Cliente {cliente_obj.nome} adicionado com sucesso!", 201