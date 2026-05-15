from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from routes.clientes import *
from routes.kits import *
from routes.orcamentos import *

if __name__ == '__main__':
    app.run(debug=True, port=5000)