from backend import app
from flask import render_template
from Database.models import *

@app.route('/novo_kit', methods=['POST'])
def novo_kit(dados):
    if not dados:
        return {'error': 'Dados do kit não fornecidos'}, 400

    kit_obj = kit(
        nome=dados.get('nome'),
        descricao=dados.get('descricao'),
        preco_c=dados.get('preco_c'),
        n_modulos=dados.get('n_modulos', 0),
        inversor=dados.get('inversor', False),
        p_modulos=dados.get('p_modulos', 0.0)
    )
    
    session.add(kit_obj)
    session.commit()

    return f"Kit {kit_obj.nome} adicionado com sucesso!", 201

@app.route('/kits')
def kits():
    return render_template('Kits.html')