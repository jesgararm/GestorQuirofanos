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
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(request.form['inputEmail'], request.form['inputPassword'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            pass
        else:
            flash('Usuario no encontrado')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

if __name__ == '__main__':
    # Se configura la aplicación
    app.config.from_object(config['development'])
    app.run(debug=True)