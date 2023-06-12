from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import InputRequired, Optional
class UpdateUser(FlaskForm):
    email = EmailField(name="email", label="Nuevo Email", render_kw={"placeholder": "email"}, validators=[Optional()])
    name = StringField(name="name", label="Nuevo Nombre", render_kw={"placeholder": "name"}, validators=[Optional()])
    submit = SubmitField("Actualizar usuario", validators=[InputRequired()])