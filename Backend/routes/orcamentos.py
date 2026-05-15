from backend import app
from flask import render_template, request, jsonify
from Database.models import *


@app.route('/get_orcamentos', methods=['GET'])
def get_orcamentos():
    return