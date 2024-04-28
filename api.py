from flask import Flask, render_template,redirect, url_for, flash
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import IngresoForm
import requests

app = Flask(__name__)
api = Api(app)

url = 'http://127.0.0.1:5000/transactions'

# Configuración de la base de datos SQLite utilizando SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'
db = SQLAlchemy(app)

# Modelo de datos para la tabla 'bank'
class BankModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    descripcion = db.Column(db.String(300))

    def __repr__(self):
        return f'<BankModel {self.id} - {self.concepto}>'

# Analizamos/"parseamos" los argumentos de la solicitud.
parser = reqparse.RequestParser()
parser.add_argument('concepto', type=str, required=True)
parser.add_argument('cantidad', type=int, required=True)
parser.add_argument('fecha', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), required=True)
parser.add_argument('descripcion', type=str)

class Bank(Resource):
    def get(self, bank_id):
        bank = BankModel.query.filter_by(id=bank_id).first()
        if bank:
            return {'id': bank.id, 'concepto': bank.concepto, 'cantidad': bank.cantidad,
                    'fecha': bank.fecha.strftime('%Y-%m-%d'), 'descripcion': bank.descripcion}
        else:
            return {'message': 'Transacción no encontrada'}, 404

    def post(self):
        args = parser.parse_args()
        concepto = args['concepto']
        cantidad = args['cantidad']
        fecha = args['fecha']
        descripcion = args['descripcion']
        new_transaction = BankModel(concepto=concepto, cantidad=cantidad, fecha=fecha, descripcion=descripcion)
        db.session.add(new_transaction)
        db.session.commit()  # Commit the transaction
        return {'id': new_transaction.id, 'concepto': concepto, 'cantidad': cantidad,
                'fecha': fecha.strftime('%Y-%m-%d'), 'descripcion': descripcion}, 201

    def put(self, bank_id):
        args = parser.parse_args()
        concepto = args['concepto']
        cantidad = args['cantidad']
        fecha = args['fecha']
        descripcion = args['descripcion']
        transaction = BankModel.query.filter_by(id=bank_id).first()
        if transaction:
            transaction.concepto = concepto
            transaction.cantidad = cantidad
            transaction.fecha = fecha
            transaction.descripcion = descripcion
            db.session.commit()
            return {'id': bank_id, 'concepto': concepto, 'cantidad': cantidad,
                    'fecha': fecha.strftime('%Y-%m-%d'), 'descripcion': descripcion}
        else:
            return {'message': 'Transacción no encontrada'}, 404

    def delete(self, bank_id):
        transaction = BankModel.query.filter_by(id=bank_id).first()
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return '', 204
        else:
            return {'message': 'Transacción no encontrada'}, 404

api.add_resource(Bank, '/transactions', '/transactions/<int:bank_id>')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_transaction', methods=['GET', 'POST'])
def transaction():
    form = IngresoForm()
    if form.validate_on_submit():
        concepto = form.concepto.data
        cantidad = form.cantidad.data
        fecha = form.fecha.data
        descripcion = form.descripcion.data
        data = {
            'concepto': concepto,
            'cantidad': cantidad,
            'fecha': fecha.strftime('%Y-%m-%d'),
            'descripcion': descripcion
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                return redirect(url_for('index'))
            else:
                flash('Error al crear la transacción', 'error')
        except requests.exceptions.RequestException as e:
            flash('Error al enviar la solicitud', 'error')
    
    return render_template('transaction.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas en la base de datos si no existen
    app.run(debug=True)