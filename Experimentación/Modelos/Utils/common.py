# Imports
import pandas as pd
import matplotlib.pyplot as plt

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
    # Eliminamos la primera columna de X, que son los ID del paciente
    X = X.drop(['NHC'], axis=1)
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

# Función que etiqueta los datos de duración de intervención
def etiquetarDatos(data):
    # Etiquetamos los datos de duración de intervención
    # 0:Menos de 60 minutos
    # 1:Entre 60 y 120 minutos
    # 2:Entre 120 y 180 minutos
    # 3:Entre 180 y 240 minutos
    # 4:Entre 240 y 300 minutos
    # 5: Más de 300 minutos
    data.loc[data['DURACIÓN'] < 60, 'DURACIÓN'] = 0
    data.loc[(data['DURACIÓN'] >= 60) & (data['DURACIÓN'] < 120), 'DURACIÓN'] = 1
    data.loc[(data['DURACIÓN'] >= 120) & (data['DURACIÓN'] < 180), 'DURACIÓN'] = 2
    data.loc[(data['DURACIÓN'] >= 180) & (data['DURACIÓN'] < 240), 'DURACIÓN'] = 3
    data.loc[(data['DURACIÓN'] >= 240) & (data['DURACIÓN'] < 300), 'DURACIÓN'] = 4
    data.loc[data['DURACIÓN'] >= 300, 'DURACIÓN'] = 5
    return data

# Función que elimina los outliers de un dataframe
def eliminarOutliers(data):
    # Eliminamos los outliers de la columna DURACIÓN
    # Limite inferior 1.5 veces por debajo del Q1
    # Limite superior 1.5 veces por encima del Q3
    Q1 = data['DURACIÓN'].quantile(0.25)
    Q3 = data['DURACIÓN'].quantile(0.75)
    IQR = Q3 - Q1
    data = data[~((data['DURACIÓN'] < (Q1 - 1.5 * IQR)) | (data['DURACIÓN'] > (Q3 + 1.5 * IQR)))]
    return data

# Función que representa los datos de duración de intervención
def representarDatos(y_pred,y):
    # Representamos los resultados
    plt.plot(y_pred, linestyle = 'dotted', color = 'red', label = 'Predicción')
    x = [i for i in range(len(y_pred))]
    plt.scatter(x, y, color = 'blue', label = 'Real')
    plt.legend()
    plt.show()