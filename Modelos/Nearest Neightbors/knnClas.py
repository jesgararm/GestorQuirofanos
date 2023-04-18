# Imports necesarios
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import matthews_corrcoef
# Importamos grid search
from sklearn.model_selection import GridSearchCV
class KNNClas():
    def __init__(self, X, y):
        self.X = X
        self.y = y
        # Usamos train test split para separar los datos
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        # Parámetros para grid search
        self.n_neighbors = [3, 5, 7, 9, 11]
        self.weights = ['uniform', 'distance']
        self.algorithm = ['auto', 'ball_tree', 'kd_tree']
        self.leaf_size = [10, 20]
        self.p = [1, 2]
        self.metric = ['minkowski', 'euclidean']
        self.metric_params = [None]
        self.n_jobs = [None]
        # Iniciamos el modelo
        self.model = KNeighborsClassifier()
        # Iniciamos el grid search
        self.grid = GridSearchCV(estimator=self.model, param_grid=dict(n_neighbors=self.n_neighbors, weights=self.weights, algorithm=self.algorithm, leaf_size=self.leaf_size, p=self.p, metric=self.metric, metric_params=self.metric_params, n_jobs=self.n_jobs), cv=5, scoring='accuracy', n_jobs=-1)
        # Entrenamos el grid search
        self.grid.fit(self.X_train, self.y_train)
        # Obtenemos los mejores parámetros
        self.best_params = self.grid.best_params_
        # Iniciamos el modelo con los mejores parámetros
        self.model = KNeighborsClassifier(n_neighbors=self.best_params['n_neighbors'], weights=self.best_params['weights'], algorithm=self.best_params['algorithm'], leaf_size=self.best_params['leaf_size'], p=self.best_params['p'], metric=self.best_params['metric'], metric_params=self.best_params['metric_params'], n_jobs=self.best_params['n_jobs'])
        # Entrenamos el modelo
        self.model.fit(self.X_train, self.y_train)
        # Obtenemos las predicciones
        self.y_pred = self.model.predict(self.X_test)
        # Obtenemos las probabilidades
        self.y_pred_proba = self.model.predict_proba(self.X_test)
    def accuracy(self):
        return accuracy_score(self.y_test, self.y_pred)

    def confusion_matrix(self):
        return confusion_matrix(self.y_test, self.y_pred)

    def classification_report(self):
        return classification_report(self.y_test, self.y_pred)

    def roc_curve(self):
        return roc_curve(self.y_test, self.y_pred_proba[:,1])

    def roc_auc_score(self):
        return roc_auc_score(self.y_test, self.y_pred_proba[:,1])

    def precision_recall_curve(self):
        return precision_recall_curve(self.y_test, self.y_pred_proba[:,1])

    def average_precision_score(self):
        return average_precision_score(self.y_test, self.y_pred_proba[:,1])

    def f1_score(self):
        return f1_score(self.y_test, self.y_pred)

    def precision_score(self):
        return precision_score(self.y_test, self.y_pred)

    def recall_score(self):
        return recall_score(self.y_test, self.y_pred)

    def cohen_kappa_score(self):
        return cohen_kappa_score(self.y_test, self.y_pred)

    def matthews_corrcoef(self):
        return matthews_corrcoef(self.y_test, self.y_pred)