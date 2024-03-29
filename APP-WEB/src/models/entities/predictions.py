# Clase que representa la entidad Predicciones de la base de datos.
class Prediccion():
    
    def __init__(self, id, id_user, date, predictions):
        self.id = id
        self.id_user = id_user
        self.fecha = date
        self.predicciones = predictions
    
    def __str__(self):
        return f"Prediccion: {self.id} {self.id_user} {self.fecha} {self.predicciones}"