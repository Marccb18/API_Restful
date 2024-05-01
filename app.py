from flask import Flask, render_template, redirect, url_for
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from forms import IngresoForm, DeudaForm
from datetime import datetime


app = Flask(__name__)
api = Api(app)

url = 'http://127.0.0.1:5000/transactions'

# Configuración de la base de datos SQLite utilizando SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'
db = SQLAlchemy(app)


class BankModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    descripcion = db.Column(db.String(300))
    
class DeudaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    deudor = db.Column(db.String(200))
    fecha = db.Column(db.Date)
    comentario = db.Column(db.String(300))
    pagada = db.Column(db.Boolean, default=False)

parser = reqparse.RequestParser()
parser.add_argument('concepto', type=str, required=True)
parser.add_argument('cantidad', type=int, required=True)
parser.add_argument('fecha', type=lambda x: datetime.strptime(x, '%d-%m-%Y'))
parser.add_argument('descripcion', type=str)

class Bank(Resource):
    def get(self, bank_id):
        bank = BankModel.query.filter_by(id=bank_id).first()
        if bank:
            return {
                'id': bank.id,
                'concepto': bank.concepto,
                'cantidad': bank.cantidad,
                'fecha': bank.fecha.strftime('%d-%m-%Y'),
                'descripcion': bank.descripcion
            }
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
        return {
            'id': new_transaction.id,
            'concepto': concepto,
            'cantidad': cantidad,
            'fecha': fecha.strftime('%d-%m-%Y'),
            'descripcion': descripcion
        }
    
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
            return {
                'id': bank_id,
                'concepto': concepto,
                'cantidad': cantidad,
                'fecha': fecha.strftime('%d-%m-%Y'),
                'descripcion': descripcion
            }
        else:
            return {'message': 'Transacción no encontrada'}, 404
    
    def delete(self, bank_id):
        transaction = BankModel.query.filter_by(id=bank_id).first()
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return '', 204
        else:
            return {'message': 'Transacción no encontrada'}
        
api.add_resource(Bank, '/transactions', '/transactions/<int:bank_id>')

deuda_parser = reqparse.RequestParser()
deuda_parser.add_argument('concepto', type=str, required=True)
deuda_parser.add_argument('cantidad', type=int, required=True)
deuda_parser.add_argument('deudor', type=str, required=True)
deuda_parser.add_argument('fecha',type=datetime, required=False)
deuda_parser.add_argument('comentario', type=str, required=False)
deuda_parser.add_argument('resuelta', type=bool, required=True)


class Deuda(Resource):
    def get(self,deuda_id):
        deuda = DeudaModel.query.get(deuda_id)
        if deuda:
            return {
                'id': deuda.id,
                'cantidad': deuda.cantidad,
                'deudor': deuda.deudor,
                'fecha': deuda.fecha.strftime('%d-%m-%Y'),
                'comentario': deuda.comentario,
                'resuelta': deuda.resuelta
            }
        else:
            return {'message': 'Deuda no encontrada'}, 404
        
    def post(self):
        args = deuda_parser.parse_args()
        concepto = args['concepto']
        cantidad = args['cantidad']
        deudor = args['deudor']
        fecha = args['fecha']
        comentario = args['comentario']
        resuelta = args['resuelta']
        nueva_deuda = DeudaModel(concepto=concepto, cantidad=cantidad, deudor=deudor, fecha=fecha, comentario=comentario, resuelta=resuelta)
        db.session.add(nueva_deuda)
        db.session.commit()
        return {
            'id': nueva_deuda.id,
            'concepto': concepto,
            'cantidad': cantidad,
            'deudor': deudor,
            'fecha': fecha.strftime('%d-%m-%Y'),
            'comentario': comentario,
            'resuelta': resuelta
        }
    
    def put(self, deuda_id):
        args = deuda_parser.parse_args()
        concepto = args['concepto']
        cantidad = args['cantidad']
        deudor  = args['deudor']
        fecha = args['fecha']
        comentario = args['comentario']
        resuelta = args['resuelta']
        deuda = DeudaModel.query.get(deuda_id)
        if deuda:
            deuda.concepto = concepto
            deuda.cantidad = cantidad
            deuda.deudor = deudor
            deuda.fecha = fecha
            deuda.comentario = comentario
            deuda.resuelta = resuelta
            return {
                'id': deuda.id,
                'concepto': concepto,
                'cantidad': cantidad,
                'deudor': deudor,
                'fecha': fecha.strftime('%d-%m-%Y'),
                'comentario': comentario,
                'resuelta': resuelta
            }
        else:
            return {'message': 'Deuda no encontrada'}, 404
        
    def delete(self,deuda_id):
        deuda = DeudaModel.query.get(deuda_id)
        if deuda:
            db.session.delete(deuda)
            db.session.commit()
            return '', 204
        else:
            return {'message': 'Deuda no encontrada'}, 404
        
api.add_resource(Deuda,'/deudas', '/deudas/<int:deuda_id>')



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)