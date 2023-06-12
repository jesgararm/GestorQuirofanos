from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
class CreateUser(FlaskForm):
    email = StringField(name="email", validators=[DataRequired()], label="Email", render_kw={"placeholder": "email"})
    password = PasswordField(name="password", validators=[DataRequired()], label="Contraseña", render_kw={"placeholder": "password"})
    name = StringField(name="name", label="Nombre", render_kw={"placeholder": "name"})
    admin = BooleanField("admin")
    submit = SubmitField("Crear usuario")