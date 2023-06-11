from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Entidad de Usuario para Login.
class User(UserMixin):
    def __init__(self, id, email, password, name="", admin=False):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.admin = admin

    def __str__(self):
        return f"User: {self.name} {self.email} {self.password}"

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @classmethod
    def generar_password(self, password):
        return generate_password_hash(password)
