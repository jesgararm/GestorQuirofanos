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
        sql = "SELECT id,email,name,created_at,updated_at,admin FROM user WHERE id = '{}'".format(
            id
        )
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(
                    id=row[0],
                    email=row[1],
                    password=None,
                    name=row[2],
                    created_at=row[3],
                    updated_at=row[4],
                    admin=row[5],
                )
            else:
                return None
        except Exception as e:
            raise e

    @classmethod
    def add_user(self, db, user):
        sql = "INSERT INTO user(email,password,name,admin) VALUES('{}','{}','{}','{}')".format(
            user.email, User.generar_password(user.password), user.name, user.admin
        )
        try:
            # Comprobamos si el usuario existe
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM user WHERE email = '{}'".format(user.email))
            row = cursor.fetchone()
            if row == None:
                cursor.execute(sql)
                db.connection.commit()
                cursor.close()
                return True
            else:
                db.connection.rollback()
                cursor.close()
                return False
        except Exception as e:
            raise e

    @classmethod
    def update_user(self, db, user):
        sql = "UPDATE user SET email='{}',name='{}', admin='{}' WHERE id='{}'".format(
            user.email, user.name, user.admin, user.id
        )
        try:
            # Comprobamos si el usuario existe
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM user WHERE id = '{}'".format(user.id))
            row = cursor.fetchone()
            if row != None:
                cursor.execute(sql)
                db.connection.commit()
                cursor.close()
                return True
            else:
                db.connection.rollback()
                cursor.close()
                return False
        except Exception as e:
            raise e

    @classmethod
    def get_users(self, db):
        sql = "SELECT id,email,name,created_at,updated_at,admin FROM user"
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append(
                    User(
                        id=row[0],
                        email=row[1],
                        password=None,
                        name=row[2],
                        created_at=row[3],
                        updated_at=row[4],
                        admin=row[5],
                    )
                )
            return users
        except Exception as e:
            raise e

    @classmethod
    def delete_user(self, db, id):
        sql = "DELETE FROM user WHERE id='{}'".format(id)
        try:
            # Comprobamos si el usuario existe
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM user WHERE id = '{}'".format(id))
            row = cursor.fetchone()
            if row != None:
                cursor.execute(sql)
                db.connection.commit()
                cursor.close()
                return True
            else:
                db.connection.rollback()
                cursor.close()
                return False
        except Exception as e:
            raise e
