# Manejo de sesiones
from . import auth_blueP as pub
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from src.models.ModelUser import ModelUser
from src.models.entities.user import User
from src import db, login_manager

@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

# Método para cerrar sesión
@pub.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# Método de login de usuario
@pub.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Comprobamos si el usuario existe
        user = User(0, request.form["inputEmail"], request.form["inputPassword"])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for("public.home"))
            else:
                flash("Contraseña incorrecta")
                return render_template("auth/login.html")
        else:
            # Si no existe, se muestra un mensaje de error
            flash("Usuario no encontrado")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")
