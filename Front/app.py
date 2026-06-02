from flask import Flask
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = Flask(__name__)

# Configurações do app a partir do .env
app.config['BACKEND_URL'] = os.getenv('BACKEND_URL', 'http://localhost:5000')
# Disponibiliza a URL base para os templates como variável `BASE`
app.jinja_env.globals['BASE'] = app.config['BACKEND_URL']

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)))