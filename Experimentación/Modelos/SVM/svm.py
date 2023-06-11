# Imports necesarios
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import joblib
# Clase que implementa el modelo de regresión SVM
class SVM:
    # Constructor
    def __init__(self, X, Y):
        # División de los datos en entrenamiento y test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        # Creación del modelo
        # Parámetros para la búsqueda de hiperparámetros
        #parameters = {'kernel':('linear', 'rbf'), 'C':[1, 3]}
        # Creación del modelo
        #svr = SVR()
        # Búsqueda de hiperparámetros
        #clf = GridSearchCV(svr, parameters)
        # Entrenamiento del modelo
        #clf.fit(self.X_train, self.y_train)
        # Obtención de los hiperparámetros
        #self.kernel = clf.best_params_['kernel']
        #self.C = clf.best_params_['C']
        # Creación del modelo con los hiperparámetros obtenidos
        self.model = SVR(kernel='rbf', C=3, gamma='auto', epsilon=.1, coef0=1)
        # Entrenamiento del modelo
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        self.mae = mean_absolute_error(self.y_test, self.y_pred)

    # Método que devuelve el error
    def get_MSE(self):
        return self.mse
    def get_MAE(self):
        return self.mae
    def get_RMSE(self):
        return np.sqrt(self.mse)
    # Método que devuelve los hiperparámetros
    def get_params(self):
        return self.kernel, self.C
    # Método que devuelve el modelo
    def get_model(self):
        return self.model
    def export_model(self, path):
        joblib.dump(self.model, path)
    def import_model(self, path):
        self.model = joblib.load(path)