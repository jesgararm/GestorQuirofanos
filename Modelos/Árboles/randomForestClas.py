# Imports de librerías
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
# Importamos gridsearch para optimizar los hiperparámetros
from sklearn.model_selection import GridSearchCV
# Importamos la función para exportar el modelo
import joblib
class RandomForestClas():
    def __init__(self, X, y, test_size=0.2, random_state=0):
        self.X = X
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=self.test_size,
                                                            random_state=self.random_state)
        self.gridSearch()
        self.train()
    def train(self):
        # Dividimos los datos en train y test
        # Creamos el modelo
        self.model =RandomForestClassifier(n_estimators=self.best_params['n_estimators'], max_features=self.best_params['max_features'], max_depth=self.best_params['max_depth'], criterion=self.best_params['criterion'])
        # Entrenamos el modelo
        self.model.fit(self.X_train, self.y_train)
        # Predecimos los valores de test
        self.y_pred = self.model.predict(self.X_test)
        # Calculamos la precisión
        self.accuracy = accuracy_score(self.y_test, self.y_pred)
        # Calculamos la matriz de confusión
        self.confusion_matrix = confusion_matrix(self.y_test, self.y_pred)
        # Calculamos el reporte de clasificación
        self.classification_report = classification_report(self.y_test, self.y_pred)
    def gridSearch(self):
        # Creamos el modelo
        self.model = RandomForestClassifier()
        self.param_grid = {'n_estimators': [10, 50, 100, 200],'max_features': ['auto', 'sqrt', 'log2'],'max_depth' : [4,5,6,7,8],'criterion' :['gini', 'entropy']}
        # Creamos el gridsearch
        self.grid = GridSearchCV(self.model, self.param_grid, cv=5, scoring='accuracy')
        # Entrenamos el gridsearch
        self.grid.fit(self.X_train, self.y_train)
        self.best_params = self.grid.best_params_
    def exportModel(self, path):
        # Exportamos el modelo
        joblib.dump(self.model, path)
    def importModel(self, path):
        # Importamos el modelo
        self.model = joblib.load(path)
    def predict(self, X):
        # Predecimos con el modelo
        return self.model.predict(X)
    def getAccuracy(self):
        return self.accuracy
    def getConfusionMatrix(self):
        return self.confusion_matrix
    def getClassificationReport(self):
        return self.classification_report