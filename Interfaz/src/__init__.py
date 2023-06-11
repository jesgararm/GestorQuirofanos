from flask import Flask, Blueprint
from flask_mysqldb import MySQL
from src.config import config
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
csrf = CSRFProtect()
db = MySQL()

def create_app():
    # Inicio de app
    app = Flask(__name__)
    # Configuración de app
    app.config.from_object(config["development"])
    db.init_app(app)
    login_manager.init_app(app)
    # Redefinimos la ruta de login
    login_manager.login_view = "auth.login"
    csrf.init_app(app)
    
    # Configuración de Blueprints
    from .public import pub as public_blueprint
    app.register_blueprint(public_blueprint)
    from .auth import auth_blueP as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
