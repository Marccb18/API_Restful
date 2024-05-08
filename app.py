from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)

# Configuración de la base de datos SQLite utilizando SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'
db = SQLAlchemy(app)


class Transaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Float)
    fecha = db.Column(db.Date)
    descripcion = db.Column(db.String(300))
    es_gasto = db.Column(db.Boolean)


class Deuda(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    concepto = db.Column(db.String(100))
    cantidad = db.Column(db.Float)
    deudor = db.Column(db.String(200))
    fecha = db.Column(db.Date)\
    comentario = db.Column(db.String(300))
    pagada = db.Column(db.Boolean, default=False)


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
    fecha_inicio_anio = datetime.now().replace(month=1, day=1).date()
    return calcular_balance_periodo(fecha_inicio_anio)


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


api.add_resource(GestionFinanzas, '/')
api.add_resource(Transacciones, '/transacciones')
api.add_resource(Deudas, '/deudas')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)