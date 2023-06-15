# Clase para organizar la agenda quirúrgica
# Es un recurso de la API
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource
from .Optimizacion.Genético.Genetico import Genetico
from .Optimizacion.Heuristicas.Utils import ActoQuirurgico, Quirofano
import common.utilities as utils
from math import ceil
class Schedule(Resource):
    # Definimos el método get
    def get(self):
        # Obtenemos los parámetros de la URL
        # Si no se especifica un valor, se asigna el valor por defecto
        n_quirofanos = int(request.args.get('n_quirofanos', 3))
        n_dias = int(request.args.get('n_dias', 5))
        ventana = int(request.args.get('ventana', 30))
        # Obtenemos el fichero de actos quirúrgicos
        file = request.files['file']
        # Comprobamos que el fichero es un csv
        if file.filename.split('.')[-1] != 'csv':
            return jsonify({'error': 'El fichero debe ser un csv'})
        # Leemos el fichero
        actos = pd.read_csv(file)
        # Comprobamos si tiene la columna DURACIÓN
        if 'DURACIÓN' not in actos.columns:
            _,actos = utils.makePred(actos)
        # Iniciamos el algoritmo
        genetico = Genetico(actos, n_quirofanos, n_dias, ventana)
        # Ejecutamos el algoritmo
        poblacion, logbook,hof = genetico.realiza_evolucion(heur=True)
        return jsonify(self.cromosomaAFenotipo(hof[0],genetico.getActosPendientes()))
    
    def cromosomaAFenotipo(self, cromosoma, actos):
        # Obtenemos los actos quirúrgicos, con su id
        # Recorremos el cromosoma
        # Obtenemos el número de días y de quirófanos
        # Buscamos el número de "A" en el cromosoma
        
        dias = cromosoma.count('B')
        quirofanos = ceil(cromosoma.count('A')/dias)
        devolver = {}
        # Iniciamos un diccionario para guardar los actos
        for i in range(dias):
            dia = "Dia " + str(i+1)
            devolver[dia] = {}
            for j in range(quirofanos):
                quirofano = "Quirofano " + str(j+1)
                devolver[dia][quirofano] = []
        # Recorremos el cromosoma
        dia_actual = 1
        quirofano_actual = 1
        while cromosoma:
            item = cromosoma.pop(0)
            dia = "Dia " + str(dia_actual)
            quirofano = "Quirofano " + str(quirofano_actual)
            if dia_actual > dias:
                break
            if item == 'A':
                quirofano_actual += 1
                if quirofano_actual > quirofanos:
                    quirofano_actual = 1
                continue
            if item == 'B':
                dia_actual += 1
                continue
            if item == 'V':
                continue
            devolver[dia][quirofano].append((actos[item].getIdPaciente(),actos[item].getDuracion()))
        return devolver
            