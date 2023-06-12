# Imports necesarios
from . import adminBP as pub
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from src import db
from src.models.ModelUser import ModelUser
from src.models.entities.user import User
from src.forms.createUser import CreateUser

# Método para el Home de un usuario
@pub.route("/home_admin")
@login_required
def home_admin():
    # Obtenemos si el usuario es admin o no
    admin = current_user.admin
    if not admin:
        return redirect(url_for("public.home"))
    return render_template("admin/home_admin.html")

@pub.route("/user_management", methods=["GET", "POST"])
@login_required
def user_management():
    admin = current_user.admin
    if not admin:
        return redirect(url_for("public.home"))
    form = CreateUser()
    # Comprobamos si el método es POST
    if request.method == "POST" and form.validate_on_submit():
        # Obtenemos los datos del formulario
        email = request.form["email"]
        print(email)
        password = request.form["password"]
        print(password)
        name = request.form["name"]
        print(name)
        # Comprobamos si se ha marcado la casilla de admin
        admin = False
        if "admin" in request.form:
            admin = True
        # Creamos el usuario
        print(admin)
        user = User(0,email, password, name, admin)
        # Actualizamos el usuario
        add = ModelUser.add_user(db, user)
        if add:
            flash("Usuario creado correctamente")
        else:
            flash("El usuario ya existe")
        # Redireccionamos a la página de gestión de usuarios
        return redirect(url_for("admin.user_management"))
    return render_template("admin/user_management.html", form = form)
