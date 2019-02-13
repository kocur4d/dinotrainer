from keras.models import Sequential
from keras.layers import Dense

import numpy as np

class Dino:
    REACT = ['none', 'up', 'down']

    def __init__(self):
        self.type = 'dino'

        # ---Setup brain as a NN
        model = Sequential()
        model.add(Dense(32, input_dim=810, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(3, activation='sigmoid'))
        self.brain = model

    # ---Load weights from file    
    def load_brain(self, filepath):
        brain.load_weights(filepath)

    # ---Save weights to a file
    def save_brain(self, filepath):
        brain.save_weights(filepath)

    # ---Make decision based on data
    # @return 'none' | 'up' | 'down'
    def react(self, X):
        result = self.brain.predict(X)
        return self.REACT[result.argmax()]
