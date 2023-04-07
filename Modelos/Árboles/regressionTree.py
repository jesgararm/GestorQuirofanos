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
import seaborn as sns
class RegressionTree:
    def __init__(self, X,y):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.tree = DecisionTreeRegressor()
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
        import matplotlib.pyplot as plt
        plt.plot(self.y_test, self.y_pred, "b.")
        plt.xlabel("Real")
        plt.ylabel("Predicted")
        plt.show()
    def getScores(self):
        return self.scores
    