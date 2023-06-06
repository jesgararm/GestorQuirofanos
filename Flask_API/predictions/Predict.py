# Clase para predecir la entrada
# Es un recurso de la API
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource
import sys
sys.path.append('../../')
import Flask_API.common.utilities as utils
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
        return jsonify(df.to_dict(orient='records'))

