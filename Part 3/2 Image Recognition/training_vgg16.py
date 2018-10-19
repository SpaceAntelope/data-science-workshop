# Import basic libraries and keras
import os
import numpy as np
from keras import applications
from keras.models import Sequential, load_model
from keras.layers import Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator

# Parameters of the model
img_width, img_height = 150, 150
train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 2000
nb_validation_samples = 800
epochs = 50
batch_size = 16

# Generator used to load the data
datagen = ImageDataGenerator(rescale=1. / 255)

# Load the VGG16 network from disk
try:
    model = load_model("vgg16_pretrained_imagenet.h5")
except:
    model = applications.VGG16(include_top=False, weights='imagenet')
    model.save("vgg16_pretrained_imagenet.h5")

# Extract bottleneck features
if not os.path.exists('bottleneck_features_train.npy'):
    generator = datagen.flow_from_directory(train_data_dir, shuffle=False,
        target_size=(img_width, img_height), batch_size=batch_size, class_mode=None)
    bottleneck_features_train = model.predict_generator(generator,
        nb_train_samples // batch_size, verbose = 1)
    np.save(open('bottleneck_features_train.npy', 'wb'), bottleneck_features_train)

if not os.path.exists('bottleneck_features_validation.npy'):
    generator = datagen.flow_from_directory(validation_data_dir,
        shuffle=False, target_size=(img_width, img_height), batch_size=batch_size, class_mode=None)
    bottleneck_features_validation = model.predict_generator(generator,
        nb_validation_samples // batch_size, verbose = 1)
    np.save(open('bottleneck_features_validation.npy', 'wb'), bottleneck_features_validation)

# Load bottleneck features
train_data = np.load(open('bottleneck_features_train.npy', 'rb'))
train_labels = np.array([0] * (nb_train_samples // 2) + [1] * (nb_train_samples // 2))

validation_data = np.load(open('bottleneck_features_validation.npy', 'rb'))
validation_labels = np.array([0] * (nb_validation_samples // 2) + [1] * (nb_validation_samples // 2))

# Use the pretrained features network and add a connected network on top
if not os.path.exists('bottleneck_fc_model.h5'):
    # Create a neural network with 2 dense layers
    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics = ['accuracy'])

    # Train the model
    model.fit(train_data, train_labels, epochs=epochs, batch_size=batch_size,
             verbose=1, validation_data=(validation_data, validation_labels))

    # Save the model
    model.save('bottleneck_fc_model.h5')
else:
    # Load the model from disk
    model = load_model('bottleneck_fc_model.h5')

score = model.evaluate(validation_data, validation_labels, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

