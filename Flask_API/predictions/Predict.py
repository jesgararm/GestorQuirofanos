# Clase para predecir la entrada
# Es un recurso de la API
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource
import joblib
from sklearn.tree import DecisionTreeRegressor
import sys
sys.path.append('../../')
import Modelos.Utils.common as utils
from Preprocesado.Codificacion import codificaEstandar
class Predict(Resource):
    def get(self):
        # Cargamos el modelo
        model = joblib.load('Flask_API/predictions/regressionTree.pkl')
        # Requerimos los parámetros
        file = request.files['file']
        if file.filename == '':
            return {"message": "No file selected"}, 400
        # Comprobamos la extensión del fichero
        if file.filename.split('.')[-1] != 'csv':
            return {"message": "File extension not allowed"}, 400
        # Leemos el fichero en un dataframe
        df, df_pred = self.extractDF(file)
        # Comprobamos que el dataframe tiene las columnas correctas
        parametros = model.feature_importances_
        if len(df_pred.columns) != len(parametros):
            return {"message": "Wrong columns"}, 400
        # Predecimos
        pred = model.predict(df_pred.values)
        # Devolvemos la predicción
        df['PREDICCIÓN'] = pred
        return jsonify(df.to_dict(orient='records'))

    def extractDF(self, file: object) -> pd.DataFrame:
        # Leemos el fichero en un dataframe
        df = pd.read_csv(file)
        # Eliminamos la columna que no se usa
        df_pred = df.drop(['NHC'], axis=1)
        # Codificamos: Cirugía Menor = 0; Cirugía Mayor = 1
        df_pred['TIPO'] = df['TIPO'].replace(['Menor', 'Mayor'], [0, 1])
        # Codificamos: Mañana = 0; Tarde = 1
        df_pred['TURNO'] = df['TURNO'].replace(['Mañana', 'Tarde'], [0, 1])
        # Codificamos: Actividad Ordinaria = 0; Continuidad Asistencial = 1
        df_pred['CARÁCTER ECONÓMICO'] = df['CARÁCTER ECONÓMICO'].replace(
            ['Actividad Ordinaria', 'Continuidad Asistencial'],
            [0, 1])
        df_pred = codificaEstandar(df_pred)
        return df, df_pred