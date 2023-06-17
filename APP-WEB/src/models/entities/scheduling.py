# Clase que representa la entidad Predicciones de la base de datos.
class Planificacion():
    
    def __init__(self, id, id_user, date, planificacion):
        self.id = id
        self.id_user = id_user
        self.fecha = date
        self.planificacion = planificacion
    
    def __str__(self):
        return f"Planificación: {self.id} {self.id_user} {self.fecha} {self.planificacion}"