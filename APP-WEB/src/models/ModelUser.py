from .entities.user import User
class ModelUser:
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id,email,password,name,admin FROM user WHERE email = '{}'".format(
                user.email
            )
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(
                    row[0],
                    row[1],
                    User.check_password(row[2], user.password),
                    row[3],
                    row[4],
                )
                return user
            else:
                return None
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(self, db, id):
        sql = "SELECT id,email,name,admin FROM user WHERE id = '{}'".format(id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as e:
            raise e
    @classmethod
    def add_user(self, db, user):
        sql = "INSERT INTO user(email,password,name,admin) VALUES('{}','{}','{}','{}')".format(user.email, User.generar_password(user.password), user.name, user.admin)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            db.connection.commit()
            cursor.close()
        except Exception as e:
            raise e
        
