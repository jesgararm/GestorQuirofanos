# Imports necesarios
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.user import User

# Se crea la aplicación
app = Flask(__name__)
db = MySQL(app)

# Método de inicio de la aplicación
@app.route("/")
def index():
    return redirect(url_for("login"))

# Método de login de usuario
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Comprobamos si el usuario existe
        user = User(request.form["inputEmail"], request.form["inputPassword"])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for("home"))
            else:
                flash("Contraseña incorrecta")
        else:
            # Si no existe, se muestra un mensaje de error
            flash("Usuario no encontrado")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

# Método para el Home de un usuario
@app.route("/home")
def home():
    return render_template("home.html")
if __name__ == "__main__":
    # Se configura la aplicación
    app.config.from_object(config['development'])
    print(db.app.config)
    app.run()
