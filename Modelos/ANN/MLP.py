# Imports necesarios
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
import numpy as np
import matplotlib.pyplot as plt
import joblib
# Clase que implementa un modelo de regresión de tipo MLP
class MLP:
    # Constructor de la clase
    def __init__(self, X, y):
        # Dividimos los datos en entrenamiento y test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Creamos la matriz de búsqueda de parámetros
        self.param_grid = {
        'hidden_layer_sizes': [(150,100,50), (120,80,40), (100,50,30)],
        'max_iter': [50, 100],
        'activation': ['tanh', 'relu','logistic'],
        'solver': ['sgd', 'adam'],
        'alpha': [0.0001, 0.05],
        'learning_rate': ['constant','adaptive'],
        'beta_1': [0.9, 0.99],
        'beta_2': [0.999, 0.9999],
        'epsilon': [1e-08, 1e-07]}
        modelo = MLPRegressor()
        self.grid = GridSearchCV(modelo, self.param_grid, n_jobs=-1, cv=5)
        # Entrenamos el modelo 
        # Seleccionamos una muestra aleatoria de 1000 elementos
        idx = np.random.choice(self.X_train.shape[0],1000,replace=False) # type: ignore
        self.X_train_muestra = self.X_train[idx,:]
        self.y_train_muestra = self.y_train[idx]
        self.grid.fit(self.X_train_muestra, self.y_train_muestra)
        # Obtenemos el mejor modelo
        self.best_params = self.grid.best_params_
        self.model = MLPRegressor(hidden_layer_sizes=self.best_params['hidden_layer_sizes'], max_iter=self.best_params['max_iter'], activation=self.best_params['activation'], solver=self.best_params['solver'], alpha=self.best_params['alpha'], learning_rate=self.best_params['learning_rate'], beta_1=self.best_params['beta_1'], beta_2=self.best_params['beta_2'], epsilon=self.best_params['epsilon']) # type: ignore
        self.model.fit(self.X_train, self.y_train)
        # Predecimos los valores de test
        self.y_pred = self.model.predict(self.X_test) # type: ignore
        # Calculamos el error cuadrático medio
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        # Calculamos el error absoluto medio
        self.mae = mean_absolute_error(self.y_test, self.y_pred)
        # Calculamos el porcentaje de error
        self.error = np.mean(np.abs((self.y_test - self.y_pred) / self.y_test)) * 100
        # Calculamos el porcentaje de acierto
        self.acierto = 100 - self.error

    # Función que devuelve el error cuadrático medio
    def getMSE(self):
        return self.mse

    # Función que devuelve el error absoluto medio
    def getMAE(self):
        return self.mae

    # Función que devuelve el root mean squared error
    def getRMSE(self):
        return np.sqrt(self.mse)
    
    # Función que devuelve el porcentaje de error
    def getError(self):
        return self.error
    # Función que devuelve el porcentaje de acierto
    def getAcierto(self):
        return self.acierto
    # Función que devuelve el modelo
    def getModel(self):
        return self.model
    # Función que devuelve las predicciones
    def getPredicciones(self):
        return self.y_pred
    # Función que devuelve los valores reales
    def getReales(self):
        return self.y_test
    # Función que guarda el modelo
    def saveModel(self, path):
        joblib.dump(self.model, path)
    # Función que carga el modelo
    def loadModel(self, path):
        self.model = joblib.load(path)
    # Función que muestra la gráfica de predicciones
    def drawPerformance(self):
        plt.plot(self.y_test, label='Real')
        plt.plot(self.y_pred, label='Predicción')
        plt.legend()
        plt.show()
    