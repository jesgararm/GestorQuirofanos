# Definimos modelo con Keras
# Importamos librerias
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import Model
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.losses import MeanSquaredLogarithmicError
import keras_tuner as kt
from kerastuner import HyperModel
class ANNHyperModel(HyperModel):
    
    def build(self, hp):
      model = Sequential()
      # Tune the number of units in the first Dense layer
      # Choose an optimal value between 32-512
      hp_units1 = hp.Int('units1', min_value=32, max_value=512, step=32)
      hp_units2 = hp.Int('units2', min_value=32, max_value=512, step=32)
      hp_units3 = hp.Int('units3', min_value=32, max_value=512, step=32)
      model.add(Dense(units=hp_units1, activation= hp.Choice("activation", ["relu", "tanh", "sigmoid"])))
      model.add(Dense(units=hp_units2, activation= hp.Choice("activation", ["relu", "tanh", "sigmoid"])))
      model.add(Dense(units=hp_units3, activation= hp.Choice("activation", ["relu", "tanh", "sigmoid"])))
      model.add(Dense(1, kernel_initializer='normal', activation='linear'))

      # Tune the learning rate for the optimizer
      # Choose an optimal value from 0.01, 0.001, or 0.0001
      hp_learning_rate = hp.Float("lr", min_value=1e-4, max_value=1e-2, sampling="log")

      model.compile(
          optimizer=Adam(learning_rate=hp_learning_rate),
          loss='mean_squared_error',
          metrics=[tf.keras.metrics.MeanSquaredError()]
      )

      return model
class kerasNeural():
    def __init__(self, X,Y):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        self.scaler = StandardScaler()
        self.scaler.fit(self.X_train)
        self.X_train = self.scaler.transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        # Definimos los hiperparámetros
        self.hypermodel = ANNHyperModel()
        self.tuner = kt.Hyperband(self.hypermodel, objective='val_mse', max_epochs=100, factor=3, directory='keras', project_name='gestorQuirofanos')
        self.tuner.search(self.X_train, self.y_train, epochs=100, validation_data=(self.X_test, self.y_test))
        self.best_hps = self.tuner.get_best_hyperparameters(num_trials=1)[0]
        self.model = self.tuner.get_best_models(num_models=1)[0]
        self.model.build(self.X_train.shape)
        self.model.compile(optimizer=Adam(learning_rate=self.best_hps.get('learning_rate')), loss=MeanSquaredLogarithmicError(), metrics=['msle'])
        self.history = self.model.fit(self.X_train, self.y_train, epochs=100, validation_data=(self.X_test, self.y_test))
        self.model.save('model.h5')
        self.model.summary()
        self.plot_loss()
    def plot_loss(self):
        plt.plot(self.history.history['loss'], label='loss')
        plt.plot(self.history.history['val_loss'], label='val_loss')
        plt.xlabel('Epoch')
        plt.ylabel('Error [MPG]')
        plt.legend()
        plt.grid(True)
        plt.show()
    def predict(self, X):
        X = self.scaler.transform(X)
        return self.model.predict(X)
    def get_best_hps(self):
        return self.best_hps
    def get_model(self):
        return self.model
    def get_history(self):
        return self.history
    def get_tuner(self):
        return self.tuner
    def get_scaler(self):
        return self.scaler
    