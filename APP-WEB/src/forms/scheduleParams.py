from flask_wtf import FlaskForm
from wtforms import IntegerRangeField, SelectField
from wtforms.validators import DataRequired, NumberRange
class ScheduleParams(FlaskForm):
    n_quirofanos = IntegerRangeField(name="n_quirofanos", label="Número de Quirófanos", validators=[DataRequired(), NumberRange(min=1, max=10)])
    n_dias = SelectField(name="n_dias", label="Número de días a programar", choices=[(5,'1 Semana'), (10,'2 Semanas'), (15,'3 Semanas'), (20,'4 Semanas')], validators=[DataRequired()])
    ventana = IntegerRangeField(name="ventana", label="Tiempo de Recambio entre Actos", validators=[DataRequired(), NumberRange(min=10, max=60)])