# Clase para organizar la agenda quirúrgica
# Es un recurso de la API
import pandas as pd
from flask import request, jsonify, Flask
from flask_restful import Resource
from .Optimizacion.Genético.Genetico import Genetico
import common.utilities as utils

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
        return jsonify(hof[0])