from flask import Flask, render_template, redirect, url_for
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from forms import IngresoForm, DeudaForm


app = Flask(__name__)
api = Api(app)

url = 'http://127.0.0.1:5000/transactions'

# Configuración de la base de datos SQLite utilizando SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)