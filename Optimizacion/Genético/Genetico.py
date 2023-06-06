import pandas as pd
from deap import base, creator, tools, algorithms
import numpy as np
import sys
sys.path.append('../')
from Optimizacion.Heuristicas.Utils import ActoQuirurgico, Heuristicas
import random
import math
import matplotlib.pyplot as plt
from Optimizacion.Genético.utilsGenetico import cromosomaAleatorio, evaluar, cruce, mutacion, fenotipoACromosoma

class Genetico():
    # Constructor de la clase
    def __init__(self, actos: pd.DataFrame, n_quirofanos = 3, n_dias = 5, ventana = 30):
        self.asignaAtributos(n_dias, n_quirofanos, ventana)
        self.procesaDatos(actos, ventana)
        self.preparaSolucion()

    def procesaDatos(self, actos, ventana):
        self.tiempos = math.floor(480 / ventana)
        self.actos_pendientes = self.iniciaActos(actos)

    def preparaSolucion(self):
        self.iniciaToolbox()
        self.stats = self.iniciaEstadisticas()
        self.iniciaHeuristicas()

    def asignaAtributos(self, n_dias, n_quirofanos, ventana):
        self.toolbox = base.Toolbox()
        self.n_quirofanos = n_quirofanos
        self.n_dias = n_dias
        self.ventana = ventana

    def iniciaHeuristicas(self):
        self.modHeur = Heuristicas(self.actos_pendientes, self.n_quirofanos, self.n_dias, self.tiempos)
        self.calculaHeuristicas()
        self.registraHeuristicas()

    def calculaHeuristicas(self):
        self.asignacionLPT,_ = self.modHeur.ejecutaHeuristica()
        self.asignacionLPTEDD,_ = self.modHeur.ejecutaHeuristica("LPTEDD")

    def registraHeuristicas(self):
        self.toolbox.register("heuristicaLPT", fenotipoACromosoma, self.asignacionLPT)
        self.toolbox.register("heuristicaLPTEDD", fenotipoACromosoma, self.asignacionLPTEDD)
        self.toolbox.register("indModelo", tools.initIterate, creator.Individual, self.toolbox.heuristicaLPT)
        self.toolbox.register("indModeloDos", tools.initIterate, creator.Individual, self.toolbox.heuristicaLPTEDD)

    def iniciaEstadisticas(self):
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        return stats
    def iniciaToolbox(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        self.iniciaPoblacion()
        self.iniciaOperadores()

    # Configura los parámetros de la población
    def iniciaPoblacion(self):
        self.toolbox.register("cromosoma", cromosomaAleatorio, tiempos=self.tiempos, quirofanos=self.n_quirofanos,
                              dias=self.n_dias, actos_pendientes = self.actos_pendientes)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.cromosoma)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def iniciaOperadores(self):
        self.toolbox.register("evaluate", evaluar, tiempos=self.tiempos, quirofanos=self.n_quirofanos, dias=self.n_dias,
                              actos_pendientes=self.actos_pendientes)
        self.toolbox.register("mate", cruce)
        self.toolbox.register("mutate", mutacion)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    # Configuramos los parámetros del algoritmo genético
    def iniciaActos(self, actos):
        # Nos quedamos sólo con el NHC, Ponderación y duración
        print(actos.head())
        df = actos[['NHC', 'PONDERACIÓN', 'DURACIÓN']]
        df['PONDERACIÓN'] = df['PONDERACIÓN'].astype(int)
        df['DURACIÓN'] = df['DURACIÓN'].astype(float)
        # Sumamos a la duración 25 minutos por paciente para tener en cuenta el tiempo de preparación
        # Se extrae de la mediana de varios artículos de revisión.
        df['DURACIÓN'] = df['DURACIÓN'] + 25
        ventana = 30
        # Dividimos la duración entre la ventana y redondeamos hacia arriba
        df['DURACIÓN'] = df['DURACIÓN'].apply(lambda x: math.ceil(x / self.ventana))
        # Creamos un set de actos quirúrgicos
        actos_pendientes = list()
        i = 0
        for elemento in df.itertuples():
            actos_pendientes.append(ActoQuirurgico(i, elemento[3], elemento[1], elemento[2]))
            i += 1
        return actos_pendientes

    # Función que ejecuta el algoritmo genético.
    def realiza_evolucion(self,n_poblacion=200, probabilidad_cruce=0.85, probabilidad_mutacion=0.15, numero_generaciones=1000, heur = False):
        contador, hof, logbook, poblacion = self.iniciaAlgoritmo(n_poblacion)
        if heur:
            self.addHeuristica(poblacion)
        # Ejecutamos el algoritmo genético
        for g in range(1, numero_generaciones):
            hijos, poblacion = self.seleccionaPob(poblacion)
            self.mutacionYCruce(hijos, probabilidad_cruce, probabilidad_mutacion)
            self.reemplazo(hijos, poblacion)
            record = self.actualizaLogbook(g, logbook, poblacion)
            # Comprobamos si el mejor individuo ha mejorado
            contador = self.actualizaContador(contador, hof, record)
            hof.update(poblacion)
            # Si no ha mejorado en 50 generaciones, paramos
            if contador == 100:
                break
        return poblacion, logbook, hof

    def addHeuristica(self, poblacion):
        ind1 = self.toolbox.indModelo()
        ind2 = self.toolbox.indModeloDos()
        # Sustituimos a dos individuos aleatorios por los individuos de las heurísticas
        poblacion[random.randint(0, len(poblacion) - 1)] = ind1
        poblacion[random.randint(0, len(poblacion) - 1)] = ind2

    def actualizaContador(self, contador, hof, record):
        if hof[0].fitness.values[0] > record['min']:
            contador = 0
        else:
            contador += 1
        return contador

    def seleccionaPob(self, poblacion):
        # Seleccionamos a la población
        poblacion = self.toolbox.select(poblacion, len(poblacion))
        # Clonamos a los individuos
        hijos = list(map(self.toolbox.clone, poblacion))
        return hijos, poblacion

    def iniciaAlgoritmo(self, n_poblacion):
        poblacion = self.toolbox.population(n=n_poblacion)
        # Evaluamos la población
        fitnesses = list(map(self.toolbox.evaluate, poblacion))
        for ind, fit in zip(poblacion, fitnesses):
            ind.fitness.values = fit
        logbook = self.iniciaLogbook(poblacion)
        # Iniciamos contador de generaciones sin mejora
        contador = 0
        hof = tools.HallOfFame(1)
        hof.update(poblacion)
        return contador, hof, logbook, poblacion

    def actualizaLogbook(self, g, logbook, poblacion):
        # Guardamos las estadísticas
        record = self.stats.compile(poblacion)
        logbook.record(gen=g, evals=len(poblacion), **record)
        print(logbook.stream)
        return record

    def iniciaLogbook(self, poblacion):
        # Inicializamos las estadísticas
        record = self.stats.compile(poblacion)
        logbook = tools.Logbook()
        logbook.header = ["gen", "evals"] + (self.stats.fields if self.stats else [])
        # Guardamos las estadísticas
        logbook.record(gen=0, evals=len(poblacion), **record)
        print(logbook.stream)
        return logbook

    def reemplazo(self, hijos, poblacion):
        # Evaluamos a los individuos con fitness inválido
        invalid_ind = [ind for ind in hijos if not ind.fitness.valid]
        fitnesses = map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        # Reemplazamos a la población
        poblacion[:] = hijos

    def mutacionYCruce(self, hijos, probabilidad_cruce, probabilidad_mutacion):
        # Aplicamos el cruce
        for hijo1, hijo2 in zip(hijos[::2], hijos[1::2]):
            if random.random() < probabilidad_cruce:
                self.toolbox.mate(hijo1, hijo2)
                del hijo1.fitness.values
                del hijo2.fitness.values
        # Aplicamos la mutación
        for hijo in hijos:
            if random.random() < probabilidad_mutacion:
                self.toolbox.mutate(hijo)
                del hijo.fitness.values

    def representaAlgoritmoGenetico(self, logbook):
        # Representamos el logbook
        gen = logbook.select("gen")
        fit_mins = logbook.select("min")
        fit_maxs = logbook.select("max")
        fit_averages = logbook.select("avg")
        fig, ax1 = plt.subplots()
        line1 = ax1.plot(gen, fit_mins, "b-", label="Fitness Mínimo")
        ax1.set_xlabel("Generación")
        ax1.set_ylabel("Fitness", color="b")
        for tl in ax1.get_yticklabels():
            tl.set_color("b")
        ax2 = ax1.twinx()
        line2 = ax2.plot(gen, fit_averages, "r-", label="Fitness Medio")
        ax2.set_ylabel("Fitness", color="r")
        for tl in ax2.get_yticklabels():
            tl.set_color("r")
        lns = line1 + line2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc="center right")
        plt.show()