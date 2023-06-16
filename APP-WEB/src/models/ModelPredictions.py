from .entities.predictions import Prediccion
from .entities.user import User

class ModelPredictions():
    @classmethod
    def addPrediction(self, user, prediction, db):
        sql = "INSERT INTO prediccion (id_user, prediccion) VALUES ('{}', '{}')".format(user.id, prediction)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as e:
            raise e
    
    @classmethod
    def getPredictions(self, db, user):
        sql = "SELECT ID,id_user,fecha,prediccion FROM prediccion WHERE id_user = {0}".format(user.id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row == None:
                return False,None
            else:
                predicciones = []
                rows = cursor.fetchall()
                for row in rows:
                    predicciones.append(Prediccion(row[0], row[1], row[2], row[3]))
                return True, predicciones
        except Exception as e:
            raise e
    
    @classmethod
    def get_prediction_by_id(self,db,id):
        sql = "SELECT ID,id_user,fecha,prediccion FROM prediccion WHERE id = {0}".format(id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row == None:
                return False,None
            else:
                return True, Prediccion(row[0], row[1], row[2], row[3])
        except Exception as e:
            raise e
    @classmethod
    def deletePrediction(self, prediction, db):
        sql = "DELETE FROM prediccion WHERE id = {}".format(prediction.id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            db.connection.commit()
        except Exception as e:
            raise e