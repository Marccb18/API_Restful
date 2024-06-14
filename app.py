from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime, timedelta
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

@app.route('/ingreso', methods=['GET','POST'])
def nuevo_ingreso():
    form = IngresoForm()
    if form.validate_on_submit():
        concepto = form.concepto.data
        cantidad = form.cantidad.data
        fecha = form.fecha.data
        descripcion = form.descripcion.data
        if cantidad >= 0:
            es_gasto = False
        else:
            es_gasto = True
        new_transaccion = Transaccion(concepto=concepto,cantidad=cantidad,fecha=fecha,descripcion=descripcion,es_gasto=es_gasto)
        db.session.add(new_transaccion)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('transaction.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)