from backend import app
from flask import render_template, request, jsonify
from Database.models import *

@app.route('/get_leads', methods=['GET'])
def get_leads():
    leads = session.query(cliente).all()
    return jsonify([{'id': lead.id, 'nome': lead.nome, 'email': lead.email, 'telefone': lead.telefone, 'cidade_UF': lead.cidade_UF} for lead in leads])

@app.route('/novo_lead', methods=['POST'])
def novo_lead():
    dados = request.get_json()      
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

@app.route('/editar_lead/<int:lead_id>', methods=['PUT'])
def editar_lead(lead_id):
    lead_ = session.query(cliente).filter(cliente.id == lead_id).first()
    if not lead_:
        return {'error': 'Cliente não encontrado'}, 404

    dados = request.get_json()
    if not dados:
        return {'error': 'Dados do cliente não fornecidos'}, 400

    for attr, value in dados.items():
        setattr(lead_, attr, value)

    session.commit()
    return f"Cliente {lead_.nome} atualizado com sucesso!", 200

@app.route('/deletar_lead/<int:lead_id>', methods=['DELETE'])
def deletar_lead(lead_id):
    lead_ = session.query(cliente).filter(cliente.id == lead_id).first()
    if not lead_:
        return {'error': 'Cliente não encontrado'}, 404

    session.delete(lead_)
    session.commit()
    return f"Cliente {lead_.nome} deletado com sucesso!", 200