# Imports necesarios
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import joblib
# Clase que implementa un modelo de regresión de tipo MLP
class MLP:
    # Constructor
    def __init__(self, X, y, hidden_layer_sizes, activation, solver, alpha, batch_size, learning_rate, learning_rate_init, power_t, max_iter, shuffle, random_state, tol, verbose, warm_start, momentum, nesterovs_momentum, early_stopping, validation_fraction, beta_1, beta_2, epsilon, n_iter_no_change):
        # Guardamos los parámetros
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.solver = solver
        self.alpha = alpha
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.learning_rate_init = learning_rate_init
        self.power_t = power_t
        self.max_iter = max_iter
        self.shuffle = shuffle
        self.random_state = random_state
        self.tol = tol
        self.verbose = verbose
        self.warm_start = warm_start
        self.momentum = momentum
        self.nesterovs_momentum = nesterovs_momentum
        self.early_stopping = early_stopping
        self.validation_fraction = validation_fraction
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.n_iter_no_change = n_iter_no_change

        # Creamos el modelo
        self.model = MLPRegressor(hidden_layer_sizes=self.hidden_layer_sizes, activation=self.activation, solver=self.solver, alpha=self.alpha, batch_size=self.batch_size, learning_rate=self.learning_rate, learning_rate_init=self.learning_rate_init, power_t=self.power_t, max_iter=self.max_iter, shuffle=self.shuffle, random_state=self.random_state, tol=self.tol, verbose=self.verbose, warm_start=self.warm_start, momentum=self.momentum, nesterovs_momentum=self.nesterovs_momentum, early_stopping=self.early_stopping, validation_fraction=self.validation_fraction, beta_1=self.beta_1, beta_2=self.beta_2, epsilon=self.epsilon, n_iter_no_change=self.n_iter_no_change)

        # Dividimos los datos en entrenamiento y test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Entrenamos el modelo
        self.model.fit(self.X_train, self.y_train)

    # Método que devuelve el error cuadrático medio
    def getMSE(self):
        return mean_squared_error(self.y_test, self.model.predict(self.X_test))
    
    # Método que devuelve el error absoluto medio
    def getMAE(self):
        return mean_absolute_error(self.y_test, self.model.predict(self.X_test))
    
    # Método que devuelve la raíz del error cuadrático medio
    def getRMSE(self):
        return mean_squared_error(self.y_test, self.model.predict(self.X_test)) ** 0.5
    
    # Método que devuelve el modelo
    def getModel(self):
        return self.model
    
    # Método quue representa el rendimiento
    def drawPerformance(self):
        plt.plot(self.y_test, color='blue', label='Real')
        plt.plot(self.model.predict(self.X_test), color='red', label='Predicción')
        plt.title('Predicción')
        plt.xlabel('Instancias')
        plt.ylabel('Tiempo')
        plt.legend()
        plt.show()
    def exportModel(self, path):
        joblib.dump(self.model, path)
    def importModel(self, path):
        self.model = joblib.load(path)

    