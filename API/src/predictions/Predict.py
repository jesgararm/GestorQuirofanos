# Clase para predecir la entrada
# Es un recurso de la API
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource
import common.utilities as utils

class Predict(Resource):
    def get(self):
        # Requerimos los parámetros
        file = request.files['file']
        if file.filename == '':
            return {"message": "No file selected"}, 400
        # Comprobamos la extensión del fichero
        if file.filename.split('.')[-1] != 'csv':
            return {"message": "File extension not allowed"}, 400
        # Leemos el fichero en un dataframe
        df = pd.read_csv(file)
        valido, df = utils.makePred(df)
        if not valido:
            return {"message": "Wrong columns"}, 400
        # Seleccionamos NHC, PONDERACIÓN, ESPECIALIDAD Y DURACIÓN
        df = df[['NHC', 'PONDERACIÓN', 'ESPECIALIDAD', 'DURACIÓN']]
        # Renombramos NHC a ID
        df = df.rename(columns={'NHC': 'ID', 'PONDERACIÓN':'PRIORIDAD', 'DURACIÓN': 'DURACION'})
        return jsonify(df.to_dict(orient='records'))

