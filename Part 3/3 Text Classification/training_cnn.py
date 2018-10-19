# Import basic libraries and keras
import os
import json
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential, load_model
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D

# Load input data
training = np.genfromtxt('15000tweets.csv', delimiter=',', skip_header=1, usecols=(1, 3), dtype=None, encoding='utf-8')

# Get tweets and sentiments (0 or 1)
train_x = [str(x[1]) for x in training]
train_y = np.asarray([x[0] for x in training])

# Use the 3000 most popular words found in our dataset
max_words = 3000

# Tokenize the data
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(train_x)
dictionary = tokenizer.word_index
# Save tokenizer dictionary to file
if not os.path.exists('dictionary.json'):
    with open('dictionary.json', 'w') as outfile:
        json.dump(tokenizer.word_index, outfile)

# For each tweet, change each token to its ID in the Tokenizer's word_index
sequences = tokenizer.texts_to_sequences(train_x)
train_x = pad_sequences(sequences, maxlen=300)

# Check if there is a pre-trained model
if not os.path.exists('cnn_model.h5'):
    # Create a neural network with 3 dense layers
    model = Sequential()
    model.add(Embedding(3000, 64, input_length=300))
    model.add(Conv1D(filters=100, kernel_size=2, padding='valid', activation='relu', strides=1))
    model.add(GlobalMaxPooling1D())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(train_x, train_y, batch_size=32, epochs=5, verbose=1, validation_split=0.1, shuffle=True)

    # Save the model
    model.save('cnn_model.h5')
else:
    # Load the model from disk
    model = load_model('cnn_model.h5')

