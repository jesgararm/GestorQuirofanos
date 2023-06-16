# Imports necesarios
from src.public import pub
from flask import render_template, redirect, url_for, request, flash
import pandas as pd
import requests
import json
import os
from flask_login import login_required, current_user
from src.forms.updateUser import UpdateUser
from src.models.ModelUser import ModelUser
from src.models.ModelPredictions import ModelPredictions
from src import db
# Método de inicio de la aplicación
@pub.route("/")
def index():
    return redirect(url_for("auth.login"))

# Método para el Home de un usuario
@pub.route("/home")
@login_required
def home():
    if current_user.admin:
        return redirect(url_for("admin.home_admin"))
    return render_template("home.html")

@pub.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html")

@pub.route("/edit_user", methods=["GET", "POST"])
@login_required
def edit_user():
    form = UpdateUser()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        if name != "":
            current_user.name = name
        if email != "":
            current_user.email = email
        if ModelUser.update_user(db, current_user):
            flash("Usuario actualizado correctamente")
        else:
            flash("Error al actualizar el usuario")
            return redirect(url_for("public.profile"))
        
    return render_template("user/edit.html", form = form)

@pub.route("/predictions")
@login_required
def predictions():
    # Obtenemos el usuario actual
    user = current_user
    # Obtenemos las predicciones
    flag, predictions = ModelPredictions.getPredictions(db, user)
    if flag:
        return render_template("user/predictions.html", pred = predictions)
    flash("No hay predicciones para este usuario")
    return render_template("user/predictions.html")

@pub.route("/upload", methods = ["POST"])
@login_required 
def upload():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if file.filename == "":
                flash("No se seleccionó ningún archivo")
                return redirect(url_for("public.predictions"))
            if not file.filename.endswith(".csv"):
                flash("El archivo debe ser de tipo .csv")
                return redirect(url_for("public.predictions"))
            file.save("src/static/uploads/" + file.filename)
            ruta = "src/static/uploads/" + file.filename
            # Llamamos a la API
            url = "http://localhost:7000/predict"
            predicciones = requests.get(url, files={"file": open(ruta, "rb")})
            flash("Predicciones realizadas correctamente")
            # Eliminamos el archivo para ahorrar espacio
            os.remove(ruta)
            df = pd.read_json(json.dumps(predicciones.json()))
            return render_template("user/predictions.html", data = df, pred = True)
    return redirect(url_for("public.predictions"))

# Definimos una vista para manejar los errores 401
@pub.errorhandler(401)
def error_401(error):
    return redirect(url_for("auth.login"))

# Definimos una vista para manejar los errores 404
@pub.errorhandler(404)
def error_404(error):
    return "<h1>Página no encontrada</h1>", 404
