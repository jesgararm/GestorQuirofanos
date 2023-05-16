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
    
    class Heuristicas:
        def __init__(self, actos_pendientes, n_quirofanos, n_dias, tiempo):
            self.actos_pendientes = actos_pendientes
            self.n_quirofanos = n_quirofanos
            self.n_dias = n_dias
            self.tiempo = tiempo
        def getActosPendientes(self):
            return self.actos_pendientes
        def getQuirofanos(self):
            return self.n_quirofanos
        def getDias(self):
            return self.n_dias
        def getTiempo(self):
            return self.tiempo
        def ordenaPacientesLPT(self):
            # Calculamos los deciles de la ponderación
            deciles = np.percentile([acto.getPrioridad() for acto in self.actos_pendientes], np.arange(0, 100, 10))
            # Creamos un diccionario con los deciles y los pacientes que pertenecen a cada uno
            diccionario = {}
            for i in range(len(deciles)):
                diccionario[i] = set()
            for acto in self.actos_pendientes:
                for i in range(len(deciles)-1):
                    if acto.getPrioridad() >= deciles[i] and acto.getPrioridad() < deciles[i+1]:
                        diccionario[i].add(acto)
                        break
                    # Si estamos en el último decil, incluimos todos los pacientes que tengan una ponderación mayor o igual
                    # al último decil
                    if i == len(deciles)-2:
                        diccionario[i+1].add(acto)
                        break
            # Ordenamos los pacientes de cada decil por duración de mayor a menor
            for i in range(len(deciles)):
                diccionario[i] = sorted(diccionario[i], key=lambda acto: acto.getDuracion(), reverse=True)
            # Creamos una lista con los pacientes ordenados de mayor decil a menor
            actos_ordenados = []
            for i in range(len(diccionario)-1, -1, -1):
                actos_ordenados += diccionario[i]
            return actos_ordenados
        
        def protectedDivision(self,x, y):
            if y == 0:
                return x
            return x / y
        
        def ordenaPacientesLPTEDD(self):
            actos_ordenados = sorted(self.actos_pendientes, key=lambda acto: self.protectedDivision(acto.getPrioridad(), acto.getDuracion()), reverse=True)
            return actos_ordenados
        
        def ejecutaHeuristica(self, criterio = "LPT"):
            # Realizamos una copia de la lista de actos pendientes
            actos_pendientes = actos_pendientes.copy()
            # Primero ordenamos los actos quirúrgicos por duración y prioridad
            if criterio == "LPT":
                actos_pendientes = self.ordenaPacientesLPT()
            elif criterio == "LPTEDD":
                actos_pendientes = self.ordenaPacientesLPTEDD()
            # Creamos una lista de quirófanos, cada uno con su día y tiempo de trabajo
            quirofanos = []
            for i in range(self.n_quirofanos):
                quirofanos.append([])
                for j in range(self.n_dias):
                    quirofanos[i].append(Quirofano(i, j,self.getTiempo()))
            # Creamos una matriz de tiempos de trabajo
            tiempos = np.zeros((self.getQuirofanos(), self.getDias()))
            # Asignamos a cada posición el tiempo de trabajo de cada quirófano
            for i in range(self.getQuirofanos()):
                for j in range(self.getDias()):
                    tiempos[i][j] = quirofanos[i][j].getTiempoLibre()
            # Asignamos los actos quirúrgicos
            for acto in actos_pendientes:
                # Buscamos el quirófano que tiene más tiempo disponible
                maximo = np.max(tiempos)
                if maximo < acto.getDuracion():
                    # Si el tiempo disponible es menor que la duración del acto, no se puede asignar
                    continue
                # Buscamos el índice del quirófano que más tiempo disponible tiene
                # En caso de que haya más de uno, nos quedamos con el primero
                maximo_index = np.where(tiempos == maximo)
                maximo_index = (maximo_index[0][0], maximo_index[1][0])
                # Asignamos el acto quirúrgico al quirófano que menos tiempo tiene asignado
                quirofanos[maximo_index[0]][maximo_index[1]].addActo(acto)
                # Actualizamos el tiempo disponible del quirófano
                tiempos[maximo_index[0]][maximo_index[1]] -= acto.getDuracion()
                # Eliminamos el acto quirúrgico de la lista de actos pendientes
                actos_pendientes.remove(acto)
            return quirofanos, actos_pendientes

