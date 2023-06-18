from .entities.scheduling import Planificacion

class ModelScheduling():
    @classmethod
    def addSchedule(self, user, planificacion, db, ventana):
        sql = "INSERT INTO planificacion (id_user, planificacion,ventana) VALUES ('{}', '{}','{}')".format(user.id, planificacion,ventana)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as e:
            raise e
    
    @classmethod
    def getSchedulings(self, db, user):
        sql = "SELECT ID,id_user,fecha,planificacion,ventana FROM planificacion WHERE id_user = {0}".format(user.id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row == None:
                return False,None
            else:
                planificaciones = []
                planificaciones.append(Planificacion(row[0], row[1], row[2], row[3],row[4]))
                rows = cursor.fetchall()
                for row in rows:
                    planificaciones.append(Planificacion(row[0], row[1], row[2], row[3],row[4]))
                return True, planificaciones
        except Exception as e:
            raise e
    
    @classmethod
    def get_schedule_by_id(self,db,id):
        sql = "SELECT ID,id_user,fecha,planificacion,ventana FROM planificacion WHERE id = {0}".format(id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if row == None:
                return False,None
            else:
                return True, Planificacion(row[0], row[1], row[2], row[3],row[4])
        except Exception as e:
            raise e
    @classmethod
    def deleteSchedule(self, planificacion, db):
        sql = "DELETE FROM planificacion WHERE id = {}".format(planificacion.id)
        try:
            cursor = db.connection.cursor()
            cursor.execute(sql)
            db.connection.commit()
        except Exception as e:
            raise e