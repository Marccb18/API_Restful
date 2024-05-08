from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


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
    fecha = db.Column(db.Date)
    comentario = db.Column(db.String(300))
    pagada = db.Column(db.Boolean, default=False)
