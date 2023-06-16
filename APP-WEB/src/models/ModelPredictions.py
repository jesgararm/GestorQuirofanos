from .entities.predictions import Predicciones
from .entities.user import User

class ModelPredictions():
    @classmethod
    def addPrediction(self, user, prediction, db):
        sql = "INSERT INTO predicciones (id_user, prediccion) VALUES ('{}', '{}')".format(user.id, prediction)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as e:
            raise e
    
    @classmethod
    def getPredictions(self, db, user):
        sql = "SELECT * FROM predicciones WHERE id_user = {0}".format(user.id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row == None:
                return False,None
            else:
                predicciones = []
                rows = row.fetchall()
                for row in rows:
                    predicciones.append(Predicciones(row[0], row[1], row[2], row[3]))
                return True, predicciones
        except Exception as e:
            raise e