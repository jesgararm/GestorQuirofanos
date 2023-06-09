class User():
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __str__(self):
        return f'User: {self.name} {self.email} {self.password}'