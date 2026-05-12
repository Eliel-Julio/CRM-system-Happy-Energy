from backend import app
from flask import render_template, request, jsonify
from Database.models import *


@app.route('/get_kits', methods=['GET'])
def get_kits():
    kits = session.query(kit).all()
    return jsonify([{
        'id': kit.id,
        'nome': kit.nome,
        'descricao': kit.descricao,
        'preco_c': kit.preco_c,
        'n_modulos': kit.n_modulos,
        'p_modulos': kit.p_modulos,
        'inversor': kit.inversor
    } for kit in kits])

@app.route('/novo_kit', methods=['POST'])
def novo_kit():
    dados = request.get_json()
    
    if not dados:
        return jsonify({'error': 'Dados do kit não fornecidos'}), 400
    print('-----------debug1-----------')
    try:
        kit_obj = kit(
            nome=dados.get('nome'),
            descricao=dados.get('descricao'),
            preco_c=dados.get('precoVenda', 0.0),
            n_modulos=dados.get('numModulos', 0),
            inversor=True,
            p_modulos=dados.get('potencia', 0.0)
        )
        print('-----------debug2-----------', kit_obj, kit_obj.nome)
    
        session.add(kit_obj)
        session.commit()
        print('-----------debug3.1-----------')

        return jsonify({'success': True, 'message': f"Kit {kit_obj.nome} adicionado com sucesso!"}), 201
    except Exception as e:
        print('-----------debug3.2-----------')
        return jsonify({'error': str(e)}), 500