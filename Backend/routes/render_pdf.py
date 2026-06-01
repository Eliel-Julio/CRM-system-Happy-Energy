from backend import app
from flask import render_template, request, jsonify, send_file
from Database.models import *
from render.render import render_proposta

@app.route('/download_orcamento/<int:orcamento_id>', methods=['GET'])
def download_orcamento(orcamento_id):
    orcamento = session.query(proposta).filter(proposta.id == orcamento_id).first()
    if not orcamento:
        return {'error': 'Orçamento não encontrado'}, 404
    try:
        orcamento_ = orcamento.__dict__
        orcamento_.pop('_sa_instance_state', None)

        buffer = render_proposta(orcamento_)

        # nome_cliente = (orcamento_.get('cliente_json',{"nome": 'anonimo'}).get('nome','Anonimo')).replace(' ', '_')
        # nome_cliente = orcamento_['cliente_json']['nome'].replace(' ', '_') 
        # nome_arquivo = f"Proposta_{orcamento_id}_{nome_cliente}.pdf"
        nome_arquivo = f"Proposta_{orcamento_id}.pdf"
        # return jsonify(orcamento_)
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nome_arquivo,
        )
    except Exception as e:
        return {'error \_/': str(e.args)}, 500