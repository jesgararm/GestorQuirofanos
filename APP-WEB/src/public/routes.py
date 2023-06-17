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
from src.models.ModelScheduling import ModelScheduling
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
        return render_template("user/predictions.html", pred = predictions, flag=True)
    flash("No hay predicciones para este usuario")
    return render_template("user/predictions.html")
@pub.route("/scheduling")
@login_required
def scheduling():
    user = current_user
    # Obtenemos las planificaciones
    flag, schedulings = ModelScheduling.getSchedulings(db, user)
    if flag:
        return render_template("user/scheduling.html", sched = schedulings, flag=True)
    flash("No hay planificaciones para este usuario")
    return render_template("user/scheduling.html")

@pub.route("/uploadScheduling", methods = ["POST"])
@login_required
def uploadScheduling():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if file.filename == "":
                flash("No se seleccionó ningún archivo")
                return redirect(url_for("public.scheduling"))
            if not file.filename.endswith(".csv"):
                flash("El archivo debe ser de tipo .csv")
                return redirect(url_for("public.scheduling"))
            file.save("src/static/uploads/" + file.filename)
            ruta = "src/static/uploads/" + file.filename
            # Llamamos a la API
            url = "http://localhost:7000/schedule"
            planificacion = requests.get(url, files={"file": open(ruta, "rb")})
            flash("Planificación realizada correctamente")
            # Eliminamos el archivo para ahorrar espacio
            os.remove(ruta)
            ModelScheduling.addSchedule(current_user, json.dumps(planificacion.json()),db)
    return redirect(url_for("public.scheduling"))

@pub.route("/showScheduling/<id>")
@login_required
def showScheduling(id):
    flag, schedule = ModelScheduling.get_schedule_by_id(db, id)
    if flag:
        df = pd.read_json(schedule.planificacion)
        print(df.index)
        return render_template("user/showScheduling.html", data = df)
    flash("No existe la planificación")
    return render_template("user/scheduling.html")

@pub.route("/deleteScheduling/<id>")
@login_required
def deleteScheduling(id):
    flag, schedule = ModelScheduling.get_schedule_by_id(db, id)
    if flag:
        ModelScheduling.deleteSchedule(schedule, db)
        flash("Planificación eliminada correctamente")
        return redirect(url_for("public.scheduling"))
    flash("No existe la planificación")
    return render_template("user/scheduling.html")

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
            ModelPredictions.addPrediction(current_user, json.dumps(predicciones.json()),db)
    return redirect(url_for("public.predictions"))

@pub.route("/prediction/<id>")
@login_required
def prediction(id):
    flag, prediction = ModelPredictions.get_prediction_by_id(db, id)
    if flag:
        df = pd.read_json(prediction.predicciones)
        return render_template("user/showPred.html", data = df)
    flash("No existe la predicción")
    return render_template("user/predictions.html")

@pub.route("/deletePred/<id>")
@login_required
def deletePred(id):
    flag, prediction = ModelPredictions.get_prediction_by_id(db, id)
    if flag:
        ModelPredictions.deletePrediction(prediction, db)
        flash("Predicción eliminada correctamente")
        return redirect(url_for("public.predictions"))
    flash("No existe la predicción")
    return render_template("user/predictions.html")

# Definimos una vista para manejar los errores 401
@pub.errorhandler(401)
def error_401(error):
    return redirect(url_for("auth.login"))

# Definimos una vista para manejar los errores 404
@pub.errorhandler(404)
def error_404(error):
    return "<h1>Página no encontrada</h1>", 404
