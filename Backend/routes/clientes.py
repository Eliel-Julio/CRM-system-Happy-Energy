from backend import app
from flask import render_template
from Database.models import *

@app.route('/novo_cliente', methods=['POST'])
def novo_cliente(dados):
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

@app.route('/kits')
def kits():
    return render_template('Kits.html')