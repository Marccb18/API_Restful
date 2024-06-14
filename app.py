from flask import Flask, request, render_template, redirect, url_for
from forms import IngresoForm, DeudaForm
from models import db, Deuda,Transaccion
from api import *

app = Flask(__name__)

# Configuración de la base de datos SQLite utilizando SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'

api.init_app(app)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)