from backend import app
from flask import render_template, request, jsonify
from Database.models import *
# from flask_cors import CORS
# CORS(app)

@app.route('/get_kits', methods=['GET'])
def get_kits():
    kits = session.query(kit).all()
    return jsonify([{
        'id': kit.id,
        'nome': kit.nome,
        'descricao': kit.descricao,
        'preco_c': kit.preco_c,

        "modulo_json":kit.modulos_json,
        "inversor_json":kit.inversor_json ,
        "estrutura_json":kit.estrutura_json,
        "garantias_json":kit.garantias_json,

    } for kit in kits])

@app.route('/novo_kit', methods=['POST'])
def novo_kit():
    dados = request.get_json()
    
    if not dados:
        return jsonify({'error': 'Dados do kit não fornecidos'}), 400
    print('-----------debug1-----------')
    try:
        print(dados.get('modulos'))
        kit_obj = kit(
            nome=dados.get('nome'),
            descricao=dados.get('descricao',""),
            preco_c=dados.get('precoVenda', 0.0),

            modulos = dados.get("modulos",""),
            inversor = dados.get("inversor","") ,
            estrutura = dados.get("estrutura",""),
            garantias = dados.get("garantias",""),
        )
    
        session.add(kit_obj)
        session.commit()

        return jsonify({'success': True, 'message': f"Kit {kit_obj.nome} adicionado com sucesso!"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/editar_kit/<int:kit_id>', methods=['PUT'])
def editar_kit(kit_id):
    kit_ = session.query(kit).filter(kit.id == kit_id).first()
    if not kit_:
        return jsonify({'error': 'Kit não encontrado'}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({'error': 'Dados do kit não fornecidos'}), 400

    for attr, value in dados.items():
        setattr(kit_, attr, value)

    session.commit()
    return jsonify({'success': True, 'message': f"Kit {kit_.nome} atualizado com sucesso!"}), 200

@app.route('/deletar_kit/<int:kit_id>', methods=['DELETE'])
def deletar_kit(kit_id):
    kit_ = session.query(kit).filter(kit.id == kit_id).first()
    if not kit_:
        return jsonify({'error': 'Kit não encontrado'}), 404

    session.delete(kit_)
    session.commit()
    return jsonify({'success': True, 'message': f"Kit {kit_.nome} deletado com sucesso!"}), 200