from backend import app
from flask import render_template, request, jsonify
from Database.models import *

@app.route('/get_leads', methods=['GET'])
def get_leads():
    leads = session.query(cliente).all()
    # leads_ = [lead.__dict__ for lead in leads]
    # leads_.pop('_sa_instance_state',None)
    # return leads_
    return jsonify([{
        'id': lead.id,
        'nome': lead.nome,
        'CPF': lead.cpf,
        'email': lead.email, 
        'telefone': lead.telefone, 
        'cidade_uf': lead.cidade_uf,
        'endereco':lead.endereco,
        } for lead in leads])

@app.route('/novo_lead', methods=['POST'])
def novo_lead():
    dados = request.get_json()      
    if not dados:
        return {'error': 'Dados do cliente não fornecidos'}, 400
    try:
        cliente_obj = cliente(
            nome=dados.get('nome'),
            cpf=dados.get('cpf'),
            email=dados.get('email'),
            telefone=dados.get('telefone'),
            cidade_uf=dados.get('cidade_uf'),
            endereco=dados.get('endereco')
        )
        
        session.add(cliente_obj)
        session.commit()

    except Exception as e:
        session.rollback()
        return {'error': str(e)}, 400

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