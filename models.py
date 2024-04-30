from app import db


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