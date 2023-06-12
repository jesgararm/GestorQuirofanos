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

@pub.route("/user_management")
@login_required
def user_management():
    admin = current_user.admin
    if not admin:
        return redirect(url_for("public.home"))
    users = ModelUser.get_users(db)
    return render_template("admin/user_management.html", users=users)

@pub.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    admin = current_user.admin
    if not admin:
        return redirect(url_for("public.home"))
    form = CreateUser()
    # Comprobamos si el método es POST
    if request.method == "POST" and form.validate_on_submit():
        # Obtenemos los datos del formulario
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        # Comprobamos si se ha marcado la casilla de admin
        admin = False
        if "admin" in request.form:
            admin = True
        # Creamos el usuario
        print(admin)
        user = User(0, email=email, password=password, name=name, admin=admin)
        # Actualizamos el usuario
        add = ModelUser.add_user(db, user)
        if add:
            flash("Usuario creado correctamente")
        else:
            flash("El usuario ya existe")
        # Redireccionamos a la página de gestión de usuarios
        return redirect(url_for("admin.add_user"))
    return render_template("admin/add_user.html", form=form)

@pub.route("/delete_user/<int:id>")
@login_required
def delete_user(id):
    admin = current_user.admin
    if not admin:
        return redirect(url_for("public.home"))
    if ModelUser.delete_user(db, id):
        flash("Usuario borrado correctamente")
    else:
        flash("Error al borrar el usuario")
    return redirect(url_for("admin.user_management"))

@pub.route("/edit_user/<int:id>")
@login_required
def edit_user(id):
    pass
