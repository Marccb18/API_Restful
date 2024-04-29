from flask import Flask, render_template, redirect, url_for, flash, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import IngresoForm, DeudaForm
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
    
class DeudaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    deudor = db.Column(db.String(200))
    fecha = db.Column(db.Date)
    comentario = db.Column(db.String(300))
    pagada = db.Column(db.Boolean, default=False)

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
        db.session.commit()
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

class SaldoActual(Resource):
    def get(self):
        transactions = BankModel.query.all()
        saldo = 0
        for transaction in transactions:
            if transaction.cantidad > 0:
                saldo += transaction.cantidad
            else:
                saldo -= abs(transaction.cantidad)
        return {'saldo': saldo}
    
api.add_resource(SaldoActual, '/transactions/saldo')

class Deuda(Resource):
    def get(self,deuda_id):
        deuda = DeudaModel.query.filter_by(id=deuda_id).first()
        if deuda:
            return {
                'id':deuda.id,
                'concepto': deuda.concepto,
                'cantidad': deuda.cantidad,
                'deudor': deuda.deudor,
                'fecha': deuda.fecha.strftime('%Y-%m-%d'),
                'comentario': deuda.comentario
            }
        else:
            return {'message': 'Deuda no encontrada'}, 404
        
    def post(self):
        args = parser.parse_args()
        concepto = args['concepto']
        cantidad = -args['cantidad']  # Las deduas se representan con cantidades negativas
        deudor = args['deudor']
        fecha = args['fecha']
        comentario = args['comentario']
        n_deuda = DeudaModel(concepto=concepto, cantidad=cantidad, deudor=deudor, fecha=fecha, comentario=comentario)
        db.session.add(n_deuda)
        db.session.commit()
        return {
            'id': n_deuda.id,
            'concepto': concepto,
            'cantidad': cantidad,
            'deudor': deudor,
            'fecha': fecha,
            'comentario': comentario
        }
    
    def put(self, deuda_id):
        args = parser.parse_args()
        concepto =args['concepto']
        cantidad = -args['cantidad']
        deudor = args['deudor']
        fecha = args['fecha']
        comentario = args['comentario']
        pagada = args['pagada']
        deuda = DeudaModel.query.filter_by(id=deuda_id).first()
        if deuda:
            deuda.concepto = concepto
            deuda.cantidad = cantidad
            deuda.deudor = deudor
            deuda.fecha = fecha
            deuda.comentario = comentario
            deuda.pagada = pagada
            db.session.commit()
            return {
                'id': deuda_id,
                'concepto': concepto,
                'cantidad': cantidad,
                'deudor': deudor,
                'fecha': fecha.strftime('%Y-%m-%d'),
                'comentario': comentario,
                'pagada': pagada
            }
        else:
            return {'message': 'Deuda no encontrada'}, 404
        
    def delete(self,deuda_id):
        deuda = DeudaModel.query.filter_by(id=deuda_id).first()
        if deuda:
            db.session.delete(deuda)
            db.session.commit()
            return '', 204
        else:
            return {'message', 'Deuda no encontrada'}, 404
        

api.add_resource(Deuda, '/transactions/deudas', '/transactions/deudas/<int:deuda_id>')
    



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

@app.route('/saldo_actual', methods=['GET'])
def saldo_actual():
    try:
        response = requests.get(url + '/saldo')
        if response.status_code == 200:
            saldo = response.json()['saldo']
            return render_template('saldo_actual.html', saldo=saldo)
        else:
            flash('Error al obtener el saldo actual', 'error')
            print("Error al obtener el saldo actual:", response.text)  # Imprimir contenido de la respuesta
    except requests.exceptions.RequestException as e:
        flash('Error al enviar la solicitud', 'error')
        print("Error al enviar la solicitud:", e)  # Imprimir excepción

    return render_template('saldo_actual.html', saldo=None)  # Pasar saldo como None si hay algún error

@app.route('/ver_deudas', methods=['GET','POST'])
def ver_deudas():
    try:
        response = requests.get(url + '/deudas')
        if response.status_code == 200:
            deudas = response.json()
            return render_template('ver_deudas.html', deudas=deudas)
        else:
            flash('Error al obtener las deudas', 'error')
            print('Error al obtener las deudas:', response.text)
    except requests.exceptions.RequestException as e:
        flash('Error al enviar la solicitud', 'error')
        print('Error al enviar la solicitud', e)

    return render_template('ver_deudas.html', deudas=None)

@app.route('/actualizar_deudas', methods=['POST'])
def actualizar_deudas():
    data = {}
    for key, value in request.form.items():
        if key.startswith('deuda_'):
            deuda_id = int(key.split('_')[1])
            pagada = True if value == 'on' else False
            data[deuda_id] = pagada

    try:
        response = requests.put(url + '/deudas', json=data)
        if response.status_code == 200:
            flash('Deudas actualizadas exitosamente', 'success')
        else:
            flash('Error al actualizar las deudas', 'error')
            print('Error al actualizar las deudas:', response.text)
    except requests.exceptions.RequestException as e:
        flash('Error al enviar la solicitud', 'error')
        print('Error al enviar la solicitud', e)

    return redirect(url_for('ver_deudas'))

@app.route('/nueva_deuda', methods=['GET', 'POST'])
def nueva_deuda():
    form = DeudaForm()  # Suponiendo que tienes un formulario llamado DeudaForm para ingresar datos de la deuda
    if form.validate_on_submit():
        concepto = form.concepto.data
        cantidad = form.cantidad.data
        deudor = form.deudor.data
        fecha = form.fecha.data
        comentario = form.comentario.data
        data = {
            'concepto': concepto,
            'cantidad': cantidad,
            'deudor': deudor,
            'fecha': fecha.strftime('%Y-%m-%d'),
            'comentario': comentario
        }
        try:
            response = requests.post('http://127.0.0.1:5000/transactions/deudas', json=data)
            if response.status_code == 200:
                flash('Deuda creada exitosamente', 'success')
            else:
                flash('Error al crear la deuda', 'error')
            return redirect(url_for('ver_deudas'))
        except requests.exceptions.RequestException as e:
            flash('Error al enviar la solicitud', 'error')
            print('Error al enviar la solicitud', e)

    return render_template('nueva_deuda.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
