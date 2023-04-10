# Imports necesarios
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt
import joblib
# Clase que implementa un modelo de regresión de tipo MLP
class MLP:
    # Constructor de la clase
    def __init__(self, X, y, hidden_layer_sizes, activation, solver, alpha, batch_size, learning_rate, learning_rate_init, power_t, max_iter, shuffle, random_state, tol, verbose, warm_start, momentum, nesterovs_momentum, early_stopping, validation_fraction, beta_1, beta_2, epsilon, n_iter_no_change):
        # Dividimos los datos en entrenamiento y test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        # Creamos el modelo
        self.model = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, alpha=alpha, batch_size=batch_size, learning_rate=learning_rate, learning_rate_init=learning_rate_init, power_t=power_t, max_iter=max_iter, shuffle=shuffle, random_state=random_state, tol=tol, verbose=verbose, warm_start=warm_start, momentum=momentum, nesterovs_momentum=nesterovs_momentum, early_stopping=early_stopping, validation_fraction=validation_fraction, beta_1=beta_1, beta_2=beta_2, epsilon=epsilon, n_iter_no_change=n_iter_no_change)
        # Entrenamos el modelo
        self.model.fit(self.X_train, self.y_train)
        # Predecimos los valores de test
        self.y_pred = self.model.predict(self.X_test)
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
    