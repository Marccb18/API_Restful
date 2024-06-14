from flask import jsonify
from flask_restful import Api, Resource, reqparse
from models import db, Transaccion,Deuda
from datetime import datetime, timedelta


api = Api()

parser = reqparse.RequestParser()
parser.add_argument('concepto', type=str, required=True)
parser.add_argument('cantidad', type=float, required=True)
parser.add_argument('fecha', type=lambda x: datetime.strptime(x, '%d-%m-%Y'))
parser.add_argument('descripcion', type=str)
parser.add_argument('es_gasto', type=bool, required=True)

deuda_parser = reqparse.RequestParser()
deuda_parser.add_argument('concepto', type=str, required=True)
deuda_parser.add_argument('cantidad', type=float, required=True)
deuda_parser.add_argument('deudor', type=str, required=True)
deuda_parser.add_argument('fecha', type=lambda x: datetime.strptime(x, '%d-%m-%Y'), required=False)
deuda_parser.add_argument('comentario', type=str, required=False)
deuda_parser.add_argument('pagada', type=bool, required=True)


class GestionFinanzas(Resource):
    def get(self):
        # Consultar el saldo actual
        saldo_actual = calcular_saldo_actual()
        # Consultar el balance de gastos
        balance_semana = calcular_balance_semana()
        balance_mes = calcular_balance_mes()
        balance_anual = calcular_balance_anual()

        return {
            'saldo_actual': saldo_actual,
            'balance_semana': balance_semana,
            'balance_mes': balance_mes,
            'balance_anio': balance_anual
        }


def calcular_saldo_actual():
    ingresos = sum(t.cantidad for t in Transaccion.query.filter_by(es_gasto=False).all())
    gastos = sum(t.cantidad for t in Transaccion.query.filter_by(es_gasto=True).all())
    saldo_actual = ingresos - gastos
    return saldo_actual


def calcular_balance_semana():
    fecha_inicio_semana = datetime.now().date() - timedelta(days=datetime.now().weekday())
    return calcular_balance_periodo(fecha_inicio_semana)


def calcular_balance_mes():
    fecha_inicio_mes = datetime.now().replace(day=1).date()
    return calcular_balance_periodo(fecha_inicio_mes)


def calcular_balance_anual():
    fecha_inicio_año = datetime.now().replace(month=1, day=1).date()
    return calcular_balance_periodo(fecha_inicio_año)


def calcular_balance_periodo(fecha_inicio):
    ingresos = sum(t.cantidad for t in Transaccion.query.filter(Transaccion.fecha >= fecha_inicio, Transaccion.es_gasto == False).all())
    gastos = sum(t.cantidad for t in Transaccion.query.filter(Transaccion.fecha >= fecha_inicio, Transaccion.es_gasto == True).all())
    balance_periodo = ingresos - gastos
    return balance_periodo


class Transacciones(Resource):
    def get(self):
        transacciones = Transaccion.query.all()
        return jsonify([{
            'id': t.id,
            'concepto': t.concepto,
            'cantidad': t.cantidad,
            'fecha': t.fecha.strftime('%d-%m-%Y'),
            'descripcion': t.descripcion,
            'es_gasto': t.es_gasto
        } for t in transacciones])

    def post(self):
        args = parser.parse_args()
        nueva_transaccion = Transaccion(**args)
        db.session.add(nueva_transaccion)
        db.session.commit()
        return {
            'id': nueva_transaccion.id,
            'concepto': nueva_transaccion.concepto,
            'cantidad': nueva_transaccion.cantidad,
            'fecha': nueva_transaccion.fecha.strftime('%d-%m-%Y'),
            'descripcion': nueva_transaccion.descripcion,
            'es_gasto': nueva_transaccion.es_gasto
        }, 201
    
    def put(self,transaccion_id):
        args = parser.parse_args()
        transaccion = Transaccion.query.get(transaccion_id)
        if not transaccion:
            return {'message': 'Transaccion no encontrada'}, 404
        
        if 'concepto' in args:
            transaccion.concepto = args['concepto']
        if 'cantidad' in args:
            transaccion.cantidad = args['cantidad']
        if 'fecha' in args:
            transaccion.fecha = args['fecha']
        if 'descripcion' in args:
            transaccion.descripcion = args['descripcion']
        if 'es_gasto' in args:
            transaccion.es_gasto = args['es_gasto']

        db.session.commit()

        return {
            'id': transaccion.id,
            'concepto': transaccion.concepto,
            'cantidad': transaccion.cantidad,
            'fecha': transaccion.fecha.strftime('%d-%m-%Y'),
            'descripcion': transaccion.descripcion,
            'es_gasto': transaccion.es_gasto
        }
    
    def delete(self, transaccion_id):
        transaccion = Transaccion.query.get(transaccion_id)
        if not transaccion:
            return {'message': 'Transacción no encontrada'}, 404

        db.session.delete(transaccion)
        db.session.commit()
        return {'message': 'Transacción eliminada correctamente'}, 200


class Deudas(Resource):
    def get(self):
        deudas = Deuda.query.all()
        return jsonify([{
            'id': d.id,
            'concepto': d.concepto,
            'cantidad': d.cantidad,
            'deudor': d.deudor,
            'fecha': d.fecha.strftime('%d-%m-%Y'),
            'comentario': d.comentario,
            'pagada': d.pagada
        } for d in deudas])

    def post(self):
        args = deuda_parser.parse_args()
        nueva_deuda = Deuda(**args)
        db.session.add(nueva_deuda)
        db.session.commit()
        return { 
            'id': nueva_deuda.id,
            'concepto': nueva_deuda.concepto,
            'cantidad': nueva_deuda.cantidad,
            'deudor': nueva_deuda.deudor,
            'fecha': nueva_deuda.fecha.strftime('%d-%m-%Y'),
            'comentario': nueva_deuda.comentario,
            'pagada': nueva_deuda.pagada
        }, 201
    
    def put(self, deuda_id):
        args = deuda_parser.parse_args()
        deuda = Deuda.query.get(deuda_id)
        if not deuda:
            return {'message': 'Deuda no encontrada'}, 404

        # Actualizar los campos modificables
        if 'concepto' in args:
            deuda.concepto = args['concepto']
        if 'cantidad' in args:
            deuda.cantidad = args['cantidad']
        if 'deudor' in args:
            deuda.deudor = args['deudor']
        if 'fecha' in args:
            deuda.fecha = args['fecha']
        if 'comentario' in args:
            deuda.comentario = args['comentario']
        if 'pagada' in args:
            deuda.pagada = args['pagada']

        db.session.commit()
        return {
            'id': deuda.id,
            'concepto': deuda.concepto,
            'cantidad': deuda.cantidad,
            'deudor': deuda.deudor,
            'fecha': deuda.fecha.strftime('%d-%m-%Y'),
            'comentario': deuda.comentario,
            'pagada': deuda.pagada
        }

    def delete(self, deuda_id):
        deuda = Deuda.query.get(deuda_id)
        if not deuda:
            return {'message': 'Deuda no encontrada'}, 404

        db.session.delete(deuda)
        db.session.commit()
        return {'message': 'Deuda eliminada correctamente'}, 200


api.add_resource(GestionFinanzas, '/finanzas')
api.add_resource(Transacciones, '/transacciones')
api.add_resource(Deudas, '/deudas')
