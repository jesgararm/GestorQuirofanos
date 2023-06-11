# Imports necesarios
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
import joblib
import matplotlib.pyplot as plt
# Clase que implementa el modelo de Random Forest
class RandomForest:
    # Constructor
    def __init__(self, X, y):
        # División de los datos en train y test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        # Creación del modelo
        self.model = RandomForestRegressor(n_estimators=100, random_state=0)
        # Entrenamiento del modelo
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)
    # Método que devuelve el error absoluto medio
    def getMAE(self):
        # Cálculo del error absoluto medio
        return mean_absolute_error(self.y_test, self.y_pred)

    # Método que devuelve el error cuadrático medio
    def getMSE(self):
        # Cálculo del error cuadrático medio
        return mean_squared_error(self.y_test, self.y_pred)

    # Método que devuelve el error cuadrático medio
    def getRMSE(self):
        # Cálculo del error cuadrático medio
        return np.sqrt(mean_squared_error(self.y_test, self.y_pred))

    # Método que devuelve el score del modelo
    def getScore(self):
        # Cálculo del score
        return self.model.score(self.X_test, self.y_test)

    # Método que devuelve el valor de la predicción
    def getPrediction(self, X):
        return self.model.predict(X)
    # Método que dibuja el gráfico de predicción
    # Método que guarda el modelo
    def exportModel(self, path):
        joblib.dump(self.model, path)
    # Método que carga el modelo
    def importModel(self, path):
        self.model = joblib.load(path)