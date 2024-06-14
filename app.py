from flask import Flask, render_template, redirect, url_for, request
from forms import IngresoForm, DeudaForm
from models import db, Deuda,Transaccion
from api import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finanzas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1234'

api.init_app(app)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nueva_transaccion', methods=['GET','POST'])
def nueva_transaccion():
    form = IngresoForm()
    if form.validate_on_submit():
        concepto = form.concepto.data
        cantidad = form.cantidad.data
        fecha = form.fecha.data
        descripcion = form.descripcion.data
        if cantidad < 0:
            es_gasto = True
        else:
            es_gasto = False
        nueva_transaccion = Transaccion(concepto=concepto,cantidad=cantidad,fecha=fecha,descripcion=descripcion, es_gasto=es_gasto)
        db.session.add(nueva_transaccion)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('transaction.html', form=form)

@app.route('/nueva_deuda', methods=['GET','POST'])
def nueva_deuda():
    form = DeudaForm()
    if form.validate_on_submit():
        concepto = form.concepto.data
        cantidad = form.cantidad.data
        deudor = form.deudor.data
        fecha = form.fecha.data if form.fecha.data else datetime.today()
        comentario = form.comentario.data
        pagada = form.pagada.data
        nueva_deuda = Deuda(concepto=concepto,cantidad=cantidad,deudor=deudor,fecha=fecha,comentario=comentario,pagada=pagada)
        db.session.add(nueva_deuda)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('nueva_deuda.html', form=form)
    
@app.route('/saldo_actual')
def saldo_actual():
    transacciones = Transaccion.query.all()
    saldo_actual = 0
    for i in transacciones:
        saldo_actual += i.cantidad
    return render_template('saldo_actual.html', saldo=saldo_actual)

@app.route('/ver_deudas', methods=['GET','POST'])
def ver_deudas():
    deudas = Deuda.query.all()
    deudas.reverse()
    if request.method == 'POST':
        for deuda in deudas:
            checkbox = f"deuda_{deuda.id}"
            deuda.pagada = checkbox in request.form
        db.session.commit()
        return redirect(url_for('ver_deudas'))
    return render_template('ver_deudas.html', deudas=deudas)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)