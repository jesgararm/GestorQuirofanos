from werkzeug.security import generate_password_hash, check_password_hash
# Entidad de Usuario para Login.
class User():
    def __init__(self, email, password, name=""):
        self.email = email
        self.password = password
        self.name = name

    def __str__(self):
        return f'User: {self.name} {self.email} {self.password}'
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)