from flask import Flask

app = Flask(__name__)

from routes.clientes import *

if __name__ == '__main__':
    app.run(debug=True, port=5000)