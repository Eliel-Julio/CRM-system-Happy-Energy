from app import app
from flask import render_template, request, jsonify
import json
import os
import requests

@app.route('/get_configs', methods=['GET'])
def get_configs():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'configs.json')

    try:
        with open(file_path) as f:
            configs = json.load(f)
        return jsonify(configs)
    except FileNotFoundError:
        return jsonify({"error": "Arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/configurações')
def configuracoes():
    req = requests.get('http://localhost:5000/get_propriedades') 
    return render_template('configurações.html', data=get_configs().json, propriedades=req)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kits')
def kits():
    return render_template('Kits.html')

@app.route('/leads')
def leads():
    return render_template('Leads.html')

@app.route('/propostas')
def propostas():
    return render_template('Propostas.html')