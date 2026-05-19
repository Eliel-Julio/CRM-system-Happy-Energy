from backend import app
from flask import render_template, request, jsonify
from Database.models import *

@app.route('/get_propriedades', methods=['GET'])
def get_propriedades():
    propriedades = session.query(propriedade).all()
    return jsonify([{
        'id': prop.id,
        'nome': prop.nome,
        'valor': prop.valor,
        'tipo': prop.tipo
    } for prop in propriedades])