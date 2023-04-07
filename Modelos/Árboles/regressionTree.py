# Clase que implementa un árbol de regresión
# Importación de librerías
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
import joblib
class RegressionTree:
    def __init__(self, X,y):
        # Creamos el diccionario de parámetros para regressionTree
        param_grid = [{'max_depth': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 'min_samples_split': [2, 3, 4, 5, 6, 7, 8, 9, 10], 'min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        tree_reg = DecisionTreeRegressor()
        # Creamos el GridSearch
        grid_search = GridSearchCV(tree_reg, param_grid, cv=5, scoring='neg_mean_squared_error', return_train_score=True)
        grid_search.fit(self.X_train, self.y_train)
        # Obtenemos los mejores parámetros
        self.best_params = grid_search.best_params_
        # Obtenemos el mejor modelo
        self.best_model = grid_search.best_estimator_
        self.tree = DecisionTreeRegressor(max_depth=self.best_params['max_depth'], min_samples_leaf=self.best_params['min_samples_leaf'], min_samples_split=self.best_params['min_samples_split'])
        self.tree.fit(self.X_train, self.y_train)
        self.y_pred = self.predict(self.X_test)
        self.mse = mean_squared_error(self.y_test, self.y_pred)
        self.rmse = np.sqrt(self.mse)
        self.scores = cross_val_score(self.tree, self.X_train, self.y_train, scoring="neg_mean_squared_error", cv=10)
        self.cross_val_predictions = cross_val_predict(self.tree, self.X_train, self.y_train, cv=10)
    def predict(self, X):
        return self.tree.predict(X)
    def getMSE(self):
        return self.mse
    def getRMSE(self):
        return self.rmse
    def drawPerformance(self):
        # Plot the results
        plt.figure()
        plt.scatter(np.arange(self.y_test.shape[0]), self.y_test, s=20, edgecolor="black", c="darkorange", label="Real")
        plt.plot(np.arange(self.y_test.shape[0]), self.y_pred, color="cornflowerblue", label="Predicted", linewidth=2)
        plt.xlabel("data")
        plt.ylabel("target")
        plt.title("Decision Tree Regression")
        plt.legend()
        plt.show()
    def getScores(self):
        return self.scores
    def exportModel(self, name):
        joblib.dump(self.tree, name)
    def importModel(self, name):
        self.tree = joblib.load(name)