from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired

class IngresoForm(FlaskForm):
    concepto = StringField('Concepto', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    fecha = DateField('Fecha')
    descripcion = StringField('Descripción (opcional)')
    submit = SubmitField('Ingresar')

class DeudaForm(FlaskForm):
    concepto = StringField('Concepto', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    deudor = StringField('Deudor', validators=[DataRequired()])
    fecha = DateField('Fecha (Opcional)')
    comentario = StringField('Comentario')
    submit = SubmitField('Aceptar')