# Imports
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
# Clase que implementa el modelo de regresión lineal
class LinearReg:
    def __init__(self, data, fit_intercept,copy_X, target,n_jobs, test_size, random_state):
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
        
        :return: Objeto de la clase LinearReg
        :rtype: LinearReg
        
        '''
        self.data = data
        self.target = target
        self.test_size = test_size
        self.random_state = random_state
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data, self.target, test_size = self.test_size, random_state = self.random_state)
        self.model = LinearRegression(fit_intercept=fit_intercept, copy_X=copy_X,n_jobs=n_jobs)
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test) # type: ignore
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        self.r2 = r2_score(self.y_test, self.y_pred)
        self.cross_val = cross_val_score(self.model, self.data, self.target, cv = 10)
        self.cross_val_pred = cross_val_predict(self.model, self.data, self.target, cv = 10)
        self.cross_val_mse = mean_squared_error(self.target, self.cross_val_pred)
        self.cross_val_r2 = r2_score(self.target, self.cross_val_pred)
        self.cross_val_rmse = np.sqrt(self.cross_val_mse)

    def getMSE(self):
        return self.mse
    def getR2(self):
        return self.r2
    def getCrossValMSE(self):
        return self.cross_val_mse
    def getCrossValR2(self):
        return self.cross_val_r2
    def getCrossValRMSE(self):
        '''
        Devuelve la raíz cuadrada del error cuadrático medio de la predicción.
        '''
        return self.cross_val_rmse
    def getCrossVal(self):
        return self.cross_val
    def getCrossValPred(self):
        return self.cross_val_pred
    def getPredictions(self):
        return self.y_pred
    def getTest(self):
        return self.y_test
    def getTrain(self):
        return self.y_train
    def getTestX(self):
        return self.X_test
    def getTrainX(self):
        return self.X_train
    def getCoef(self):
        return self.model.coef_
    def getIntercept(self):
        return self.model.intercept_
    def getScore(self):
        '''
        Devuelve el coeficiente de determinación R^2 de la predicción.
        El mejor puntaje posible es 1.0
        '''
        return self.model.score(self.X_test, self.y_test)
    def getParams(self):
        return self.model.get_params()
    def getModel(self):
        return self.model