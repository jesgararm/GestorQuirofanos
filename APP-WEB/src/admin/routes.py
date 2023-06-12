# Imports necesarios
from . import adminBP as pub
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from src import db
from src.models.ModelUser import ModelUser
from src.models.entities.user import User
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
    # Comprobamos si el método es POST
    if request.method == "POST":
        # Obtenemos los datos del formulario
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        admin = request.form["admin"]
        # Comprobamos si el usuario es admin
        if admin == "on":
            admin = True
        else:
            admin = False
        # Creamos el usuario
        user = User(email, password, name, admin)
        # Actualizamos el usuario
        ModelUser.add_user(db, user)
        # Redireccionamos a la página de gestión de usuarios
        return redirect(url_for("admin.user_management"))
    return render_template("admin/user_management.html")
