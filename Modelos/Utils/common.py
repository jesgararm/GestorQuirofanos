# Imports
import pandas as pd
# Función que devuelve un dataframe con los datos de un fichero excel
def FileToDataframe(path):
    df = pd.read_excel(path)
    return df
# Función que divide el dataframe en X e Y para los modelos
def divideData(data):
    # Separamos los datos en X e Y
    # Y será la columna de duración de la intervención
    # X será el resto de columnas
    X = data.drop(['DURACIÓN'], axis=1)
    Y = data['DURACIÓN']
    # Eliminamos las dos primeras columnas de X, que son los ID del paciente
    X = X.drop(['Unnamed: 0', 'NHC'], axis=1)
    X = X.values
    Y = Y.values
    return X, Y

# Función que divide el DataFrame ampliado en X e Y para los modelos
def divideDataAmpli(data):
    # Eliminamos las filas que NO son números en Código diagnóstico
    data = data[data['Código diagnóstico'].apply(lambda x: isinstance(x, (int, float)))]
    # Convertimos a float
    data['Código diagnóstico'] = data['Código diagnóstico'].astype(float)
    # Eliminamos nulos
    data = data.dropna()
    # Separamos los datos en X e Y
    # Y será la columna de duración de la intervención
    # X será el resto de columnas
    X = data.drop(['DURACIÓN'], axis=1)
    Y = data['DURACIÓN']
    # Eliminamos la primera columna de X, que es el ID del paciente
    X = X.drop(['NHC'], axis=1)
    X = X.values
    Y = Y.values
    return X, Y
    