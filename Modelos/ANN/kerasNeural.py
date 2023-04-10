# Definimos modelo con Keras
# Importamos librerias
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras_tuner import Hyperband
from keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
# Definimos modelo
def build_model(hp):
    # Definimos modelo
    model = Sequential()
    # Definimos capas ocultas
    for i in range(hp.Int('num_layers', 2, 20)):
        model.add(Dense(units=hp.Int('units_' + str(i),
                                     min_value=32,
                                     max_value=512,
                                     step=32),
                        activation='relu'))
    # Definimos capa de salida
    model.add(Dense(1, activation='linear'))
    # Compilamos modelo
    model.compile(
        optimizer=Adam(
            hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])),
        loss='mean_absolute_error',
        metrics=['mean_absolute_error'])
    return model
def get_Tuner():
    # Definimos tuner
    tuner = Hyperband(build_model, objective='val_mean_absolute_error',directory='keras',project_name='gestorQuirofanos',max_epochs=10)
    return tuner
# Función que entrena el modelo
def trainModel(X, Y, tuner):
    # Entrenamos modelo
    tuner.search(X, Y, epochs=5, validation_split=0.2)
    # Guardamos el mejor modelo
    best_model = tuner.get_best_models(num_models=1)[0]
    best_model.save('keras/gestorQuirofanos/best_model.h5')
    return best_model

class KerasNeural:
    def __init__(self,X,Y):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        self.tuner = get_Tuner()
        self.model = trainModel(X_train, Y_train, self.tuner)
        self.Y_test = Y_test
        self.Y_pred = self.model.predict(X_test)
        self.mae = mean_absolute_error(self.Y_test, self.Y_pred)
        self.mse = mean_squared_error(self.Y_test, self.Y_pred)
    def getMAE(self):
        return self.mae
    def getMSE(self):
        return self.mse
    def getRMSE(self):
        return self.mse**0.5
    def predict(self, X):
        return self.model.predict(X)