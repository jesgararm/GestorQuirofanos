# Imports necesarios
from . import adminBP as pub
from flask import render_template
from flask_login import login_required

# Método para el Home de un usuario
@pub.route("/home_admin")
@login_required
def home_admin():
    return render_template("admin/home_admin.html")
