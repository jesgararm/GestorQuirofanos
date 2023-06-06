# Funciones comunes a ambas API
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeRegressor
from Preprocesado.Codificacion import codificaEstandar
def makePred(df):
    df, df_pred = extractDF(df)
    # Cargamos el modelo
    model = joblib.load('Flask_API/predictions/regressionTree.pkl')
    # Comprobamos que el dataframe tiene las columnas correctas
    parametros = model.feature_importances_
    if len(df_pred.columns) != len(parametros):
        return False, df
    # Predecimos
    pred = model.predict(df_pred.values)
    # Devolvemos la predicción
    df['DURACIÓN'] = pred
    return True, df
def extractDF(df:pd.DataFrame) -> pd.DataFrame:
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