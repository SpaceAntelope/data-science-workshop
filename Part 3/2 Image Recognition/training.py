# Import basic libraries and keras
import os
from keras import backend as K
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential, load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dropout, Flatten, Dense

# Parameters of the model
img_width, img_height = 150, 150
train_data_dir = 'data/train'
validation_data_dir = 'data/validation'
nb_train_samples = 2000
nb_validation_samples = 800
epochs = 50
batch_size = 16

# Use the image data format of Tensorflow
input_shape = (img_width, img_height, 3)

# Check if there is a pre-trained model
if not os.path.exists('model.h5'):
    # Create a neural network with 3 convolutional layers and 2 dense layers
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3)), activation='relu')
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3)), activation='relu')
    model.add(MaxPooling2D(pool_size=(2, 2)))
    
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    
    model.summary()
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    
    # Perform augmentation
    train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2,
                                       zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    
    # Train the model
    train_generator = train_datagen.flow_from_directory(train_data_dir, 
        target_size=(img_width, img_height), batch_size=batch_size, class_mode='binary')
    validation_generator = test_datagen.flow_from_directory(validation_data_dir,
        target_size=(img_width, img_height), batch_size=batch_size, class_mode='binary')
    model.fit_generator(train_generator, steps_per_epoch=nb_train_samples // batch_size,
        epochs=epochs, validation_data=validation_generator,
        validation_steps=nb_validation_samples // batch_size)
    
    # Save the model
    model.save('model.h5')
else:
    # Load the model from disk
    model = load_model('model.h5')

test_datagen = ImageDataGenerator(rescale=1. / 255)
validation_generator = test_datagen.flow_from_directory(validation_data_dir,
    target_size=(img_width, img_height), batch_size=batch_size, class_mode='binary')
score = model.evaluate_generator(validation_generator, steps=nb_validation_samples // batch_size)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
