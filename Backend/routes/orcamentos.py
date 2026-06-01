from backend import app
from flask import render_template, request, jsonify
from Database.models import *


@app.route('/get_orcamentos', methods=['GET'])
def get_orcamentos():
    orcamentos = session.query(proposta).all()
    return jsonify([{
        'id': orcamento.id,
        'cliente_id': orcamento.cliente_id,
        'kit_id': orcamento.kit_id,
        'valor_total': orcamento.valor_total,
        'data': orcamento.data,

        'kit_json': orcamento.kit_json,
        'cliente_json': orcamento.cliente_json,
        'consts': orcamento.consts,

        'prazo_instalacao':orcamento.prazoprazo_instalacao,
        'condicao_pgto':orcamento.consdicao_pgto,
        'validade_proposta':orcamento.validade_proposta,
        'forma_pgto':orcamento.forma_pgto,

    } for orcamento in orcamentos])

@app.route('/novo_orcamento', methods=['POST'])
def novo_orcamento():
    dados = request.get_json()
    if not dados:
        return jsonify({'error': 'Dados do orçamento não fornecidos'}), 400
    try:
        orcamento_obj = proposta(
            cliente_id=dados.get('cliente_id'),
            kit_id=dados.get('kit_id'),
            prazo_instalacao=dados.get('prazo_instalacao', 60),
            consdicao_pgto=dados.get('condicao_pgto', ''),
            validade_proposta=dados.get('validade_proposta', 30),
            forma_pgto=dados.get('forma_pgto', '')
        )
    
        session.add(orcamento_obj)
        session.commit()

        return jsonify({'success': True, 'message': f"Orçamento <<{orcamento_obj.id}>> para cliente {orcamento_obj.cliente_json['nome']} adicionado com sucesso!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/editar_orcamento/<int:orcamento_id>', methods=['PUT'])
def editar_orcamento(orcamento_id):
    orcamento = session.query(proposta).filter_by(id=orcamento_id).first()
    if not orcamento:
        return jsonify({'error': 'Orçamento não encontrado'}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({'error': 'Dados do orçamento não fornecidos'}), 400

    try:
        orcamento.cliente_id = dados.get('cliente_id', orcamento.cliente_id)
        orcamento.kit_id = dados.get('kit_id', orcamento.kit_id)
        orcamento.prazoprazo_instalacao = dados.get('prazo_instalacao', orcamento.prazoprazo_instalacao)
        orcamento.consdicao_pgto = dados.get('condicao_pgto', orcamento.consdicao_pgto)
        orcamento.validade_proposta = dados.get('validade_proposta', orcamento.validade_proposta)
        orcamento.forma_pgto = dados.get('forma_pgto', orcamento.forma_pgto)

        session.commit()
        return jsonify({'success': True, 'message': f"Orçamento <<{orcamento.id}>> para cliente {orcamento.cliente_json['nome']} atualizado com sucesso!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/deletar_orcamento/<int:orcamento_id>', methods=['DELETE'])
def deletar_orcamento(orcamento_id):
    orcamento = session.query(proposta).filter_by(id=orcamento_id).first()
    if not orcamento:
        return jsonify({'error': 'Orçamento não encontrado'}), 404

    try:
        session.delete(orcamento)
        session.commit()
        return jsonify({'success': True, 'message': f"Orçamento <<{orcamento.id}>> para cliente {orcamento.cliente_json['nome']} deletado com sucesso!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400