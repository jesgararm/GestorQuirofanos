from .entities.user import User
class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
           cursor = db.connection.cursor()
           sql = "SELECT * FROM user WHERE email = '{}'".format(user.email) 
           cursor.execute(sql)
           row = cursor.fetchone()
           if row != None:
                user = User(row[0], User.check_password(row[1], user.password), row[2])
                return user
           else:
            return None
        except Exception as e:
            raise e

