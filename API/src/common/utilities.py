# Funciones comunes a ambas API
import pandas as pd
import joblib
import os
def makePred(df):
    df, df_pred = extractDF(df)
    # Cargamos el modelo
    ruta = os.path.dirname(os.path.abspath(__file__))
    # Añadimos el nombre del modelo
    ruta = os.path.join(ruta, 'regressionTree.pkl')
    model = joblib.load(ruta)
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

def codificaEstandar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Codifica los datos de entrada en un formato estandarizado
    """
    # Establecemos la columna TIPO como int64
    df['TIPO'] = df['TIPO'].astype('int64')
    # Usamos One Hot Enconding para codificar la columna ESPECIALIDAD
    df['ESPECIALIDAD'] = df['ESPECIALIDAD'].astype('category')
    df = pd.get_dummies(df, columns=['ESPECIALIDAD'])
    return df