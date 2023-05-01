from deap import base, creator, tools, algorithms
import random
# Tenemos por un lado un listado de pacientes y por otro un listado de quirófanos
# Cada quirófano contiene una lista de horas en las que se puede operar
# Cada paciente tiene una duración de la operación.

class Paciente:
    def __init__(self, nombre, duracion):
        self.nombre = nombre
        self.duracion = duracion
class Quirofano:
    def __init__(self, nombre, horas):
        self.nombre = nombre
        self.horas = horas
    def __str__(self):
        return self.nombre
    def __repr__(self):
        return self.nombre
    def __eq__(self, other):
        return self.nombre == other.nombre
    def __hash__(self):
        return hash(self.nombre)
class Horas:
    def __init__(self, horaInicio, horaFin):
        self.horaInicio = horaInicio
        self.horaFin = horaFin
    def __str__(self):
        return str(self.horaInicio) + " - " + str(self.horaFin)
    def __repr__(self):
        return str(self.horaInicio) + " - " + str(self.horaFin)
    def __eq__(self, other):
        return self.horaInicio == other.horaInicio and self.horaFin == other.horaFin
    def __hash__(self):
        return hash((self.horaInicio, self.horaFin))
class Operacion:
    def __init__(self, paciente, quirofano, horaInicio, horaFin):
        self.paciente = paciente
        self.quirofano = quirofano
        self.horaInicio = horaInicio
        self.horaFin = horaFin
    def __str__(self):
        return self.paciente.nombre + " " + self.quirofano.nombre + " " + str(self.horaInicio) + " - " + str(self.horaFin)
    def __repr__(self):
        return self.paciente.nombre + " " + self.quirofano.nombre + " " + str(self.horaInicio) + " - " + str(self.horaFin)
    def __eq__(self, other):
        return self.paciente == other.paciente and self.quirofano == other.quirofano and self.horaInicio == other.horaInicio and self.horaFin == other.horaFin
    def __hash__(self):
        return hash((self.paciente, self.quirofano, self.horaInicio, self.horaFin))

