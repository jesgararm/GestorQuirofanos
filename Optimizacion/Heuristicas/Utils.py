import random
import numpy as np

# Clase que representa un acto quirúrgico.
# Contiene el id del acto, la duración y el id del paciente.
class ActoQuirurgico:
    def __init__(self, id, duracion, idPaciente, prioridad):
        self.id = id
        self.duracion = duracion
        self.idPaciente = idPaciente
        self.prioridad = prioridad
    def getId(self):
        return self.id
    def getDuracion(self):
        return self.duracion
    def getIdPaciente(self):
        return self.idPaciente
    def getPrioridad(self):
        return self.prioridad
    
# Clase que representa un Quirófano
# Contiene el id del quirófano, el día y el tiempo de trabajo.
class Quirofano:
    def __init__(self, id, dia, tiempo):
        self.id = id
        self.dia = dia
        self.tiempo = tiempo
        self.pacientes = []
    def getId(self):
        return self.id
    def getDia(self):
        return self.dia
    def getTiempo(self):
        return self.tiempo
    def getActos(self):
        return self.pacientes
    def addActo(self, paciente):
        self.pacientes.append(paciente)
    def removeActo(self, paciente):
        self.pacientes.remove(paciente)
    def getTiempoOcupado(self):
        tiempo = 0
        for paciente in self.pacientes:
            tiempo += paciente.getDuracion()
        return tiempo
    def getTiempoLibre(self):
        return self.tiempo - self.getTiempoOcupado()

