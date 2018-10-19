# Import basic libraries and keras
import numpy as np
from keras.models import load_model

# Load the model
model = load_model('cnn_model.h5')

# Read the MNIST data and get test
f = np.load('mnist.npz')
x_test, y_test = f['x_test'], f['y_test']
f.close()

# Process the images as in training
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_test = x_test.astype('float32')
x_test /= 255

# Make predictions
predictions = model.predict_classes(x_test, verbose=0)
correct_indices = np.nonzero(predictions == y_test)[0]
incorrect_indices = np.nonzero(predictions != y_test)[0]
print("Correct: %d" %len(correct_indices))
print("Incorrect: %d" %len(incorrect_indices))

# Optionally plot some images
#import matplotlib.pyplot as plt
#plt.figure()
#for i, correct in enumerate(correct_indices[:9]):
#    plt.subplot(3,3,i+1)
#    plt.tight_layout()
#    plt.imshow(x_test[correct].reshape(28,28), cmap='gray', interpolation='none')
#    plt.title("Predicted {}, Class {}".format(predictions[correct], y_test[correct]))
#    
#plt.figure()
#for i, incorrect in enumerate(incorrect_indices[:9]):
#    plt.subplot(3,3,i+1)
#    plt.tight_layout()
#    plt.imshow(x_test[incorrect].reshape(28,28), cmap='gray', interpolation='none')
#    plt.title("Predicted {}, Class {}".format(predictions[incorrect], y_test[incorrect]))

