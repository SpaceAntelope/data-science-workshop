import os
import matplotlib.pyplot as plt
from keras.optimizers import sgd
from keras.layers.core import Dense
from keras.models import Sequential, load_model

from qcatch import Catch
from qlearning import train, test

plt.ion()
plt.show()

# parameters
max_memory = 500 # Maximum number of experiences we are storing
batch_size = 1 # Number of experiences we use for training per batch
grid_size = 10 # Size of the playing field

# Check if there is a pre-trained model
if not os.path.exists('model.h5'):
    model = Sequential()
    model.add(Dense(100, input_shape=(grid_size**2,), activation='relu'))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(3)) # There are 3 actions: [move_left, stay, move_right]
    model.compile(sgd(lr=.1), "mse")
    model.summary()
    
    # Train by playing the game - change visualize to True to also visualize the training
    env = Catch(grid_size)
    epochs = 5000
    model = train(model, epochs, env, max_memory, batch_size, verbose=1, visualize=False)

    # Save the model
    model.save('model.h5')
else:
    # Load the model from disk
    model = load_model('model.h5')

# Play game
env = Catch(grid_size)
test(model, env)
