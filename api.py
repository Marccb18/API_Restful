from flask_restful import Resource, reqparse
from models import BankModel, DeudaModel
from app import api


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