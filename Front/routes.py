from app import app
from flask import render_template

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