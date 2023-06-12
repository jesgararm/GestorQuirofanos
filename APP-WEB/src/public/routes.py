# Imports necesarios
from src.public import pub
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

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
# Definimos una vista para manejar los errores 401
@pub.errorhandler(401)
def error_401(error):
    return redirect(url_for("auth.login"))

# Definimos una vista para manejar los errores 404
@pub.errorhandler(404)
def error_404(error):
    return "<h1>Página no encontrada</h1>", 404
