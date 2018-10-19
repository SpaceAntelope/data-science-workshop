# Import basic libraries and keras
from scipy.misc import imresize
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from sklearn.metrics import classification_report
from keras import backend as K
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, load_img

# Parameters of the model
img_width, img_height = 150, 150
nb_test_samples = 800
batch_size = 16

# Load the model from disk
model = load_model('model.h5')

# Use the image data format of Tensorflow
input_shape = (img_width, img_height, 3)

# Run on test set
def run_on_test_set(test_set_path):
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_generator = test_datagen.flow_from_directory(test_set_path, shuffle = False,
        target_size=(img_width, img_height), batch_size=batch_size, class_mode='binary')
    predictions = model.predict_generator(test_generator, steps=nb_test_samples // batch_size)
    truevalues = [0] * 400 + [1] * 400
    predictedvalues = [0 if p < 0.5 else 1 for p in predictions]
    print(classification_report(truevalues, predictedvalues))

# Classify an image and optionally show it
def classify_image(image_path, plot = True):
    img = load_img(image_path)
    test_x = imresize(img, size=(img_height, img_width)).reshape(input_shape)
    test_x = test_x.reshape((1,) + test_x.shape)
    test_x = test_x / 255.0
    prediction = model.predict(test_x)
    predictedvalue = "cat" if prediction < 0.5 else "dog"
    
    if plot:
        img=mpimg.imread(image_path)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.imshow(img)
        ax.set_title("This is a " + predictedvalue)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        plt.show()

    return predictedvalue

run_on_test_set('data/test')
classify_image('data/test/dogs/dog.1440.jpg')
