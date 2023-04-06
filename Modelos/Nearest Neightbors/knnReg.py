# Importamos las librerías necesarias
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
import numpy as np
# Clase que implementa el modelo de KNN Regresión
class KNNReg:
    def __init__(self, data,target, test_size, random_state):
        '''
        Constructor de la clase
        :param data: Datos de entrada
        :param target: Datos de salida
        :param test_size: Porcentaje de datos de entrada que se usan para test
        :param random_state: Semilla para la generación de números aleatorios
        
        :type data: numpy.ndarray
        :type target: numpy.ndarray
        :type test_size: float
        :type random_state: int
        
        :return: Objeto de la clase KNNReg
        :rtype: KNNReg
        
        '''
        self.data = data
        self.target = target
        self.test_size = test_size
        self.random_state = random_state
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data, self.target, test_size = self.test_size, random_state = self.random_state)
        # Creamos el modelo
        self.model = KNeighborsRegressor()
        # Creamos el grid de parámetros
        self.param_grid = {'n_neighbors': np.arange(1, 15), 'weights': ['uniform', 'distance'], 'metric': ['euclidean', 'manhattan'], 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']}
        # Creamos el grid search
        self.grid = GridSearchCV(self.model, self.param_grid, cv=10, scoring='neg_mean_squared_error')
        # Entrenamos el modelo
        self.grid.fit(self.X_train, self.y_train)
        # Obtenemos los mejores parámetros
        self.best_params = self.grid.best_params_
        # Creamos el modelo con los mejores parámetros
        self.model = KNeighborsRegressor(n_neighbors = self.best_params['n_neighbors'], weights = self.best_params['weights'], metric = self.best_params['metric'], algorithm = self.best_params['algorithm'])
        #self.model = KNeighborsRegressor(n_neighbors = 3, weights = 'uniform', metric = 'euclidean', algorithm = 'auto')
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test) # type: ignore
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        self.cross_val = cross_val_score(self.model, self.data, self.target, cv = 10)
        self.cross_val_pred = cross_val_predict(self.model, self.data, self.target, cv = 10)
        self.cross_val_mse = mean_squared_error(self.target, self.cross_val_pred)
        self.cross_val_rmse = np.sqrt(self.cross_val_mse)
        self.root_mean_squared_error = np.sqrt(self.mse)
    def getMSE(self):
        return self.mse
    def getCrossValMSE(self):
        return self.cross_val_mse
    def getCrossValPredMSE(self):
        return self.cross_val_pred
    def getCrossValRMSE(self):
        return self.cross_val_rmse
    def exportModel(self, filename):
        from joblib import dump
        dump(self.model, filename)