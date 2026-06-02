from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from routes.clientes import *
from routes.kits import *
from routes.orcamentos import *
from routes.prpriedades import *
from routes.render_pdf import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)