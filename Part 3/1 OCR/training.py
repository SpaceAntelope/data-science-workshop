# Import basic libraries and keras
import os
import keras
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import Sequential, load_model

# Read the MNIST data and split to train and test
f = np.load('mnist.npz')
x_train, y_train = f['x_train'], f['y_train']
x_test, y_test = f['x_test'], f['y_test']
f.close()

# Optionally plot some images
#import matplotlib.pyplot as plt
#fig = plt.figure()
#for i in range(9):
#  plt.subplot(3,3,i+1)
#  plt.tight_layout()
#  plt.imshow(x_train[i], cmap='gray', interpolation='none')
#  plt.title("Digit: {}".format(y_train[i]))
#  plt.xticks([])
#  plt.yticks([])

# Reshape from (num_samples, 28, 28) to (num_samples, 784)
x_train = x_train.reshape(x_train.shape[0], 784)
x_test = x_test.reshape(x_test.shape[0], 784)
# Change type from int to float and normalize to [0, 1]
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

# Optionally check the number of samples
#print(x_train.shape[0], 'train samples')
#print(x_test.shape[0], 'test samples')

# Convert class vectors to binary class matrices (transform the problem to multi-class classification)
num_classes = 10
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Check if there is a pre-trained model
if not os.path.exists('model.h5'):
    # Create a neural network with 3 dense layers
    model = Sequential()
    model.add(Dense(512, activation='relu', input_shape=(784,)))
    model.add(Dropout(0.2))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation='softmax'))
    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train, batch_size=128, epochs=20, verbose=1,
              validation_data=(x_test, y_test))

    # Save the model
    model.save('model.h5')

else:
    # Load the model from disk
    model = load_model('model.h5')

# Get loss and accuracy on validation set
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
