# Definimos modelo con Keras
# Importamos librerias
from os.path import normpath
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras_tuner import Hyperband
from keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import keras_tuner
class MyHyperModel(keras_tuner.HyperModel):
    def build(self, hp):
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

class KerasNeural:
    def __init__(self,X,Y):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        self.tuner = Hyperband(MyHyperModel(),max_epochs=10, objective='mean_absolute_error', directory="keras", project_name="gestorQuirofanos")
        self.tuner.search(X_train, Y_train, epochs=10, validation_data=(X_test, Y_test))
        self.model = self.tuner.get_best_models(num_models=1)[0]
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