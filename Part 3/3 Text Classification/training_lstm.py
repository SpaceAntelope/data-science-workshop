# Import basic libraries and keras
import os
import json
import keras
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential, load_model
from keras.layers import Dense, Embedding, LSTM
from keras.preprocessing.sequence import pad_sequences
from dataload import load_data

# Load input data and labels (0 to 4)
train_x, train_y = load_data()

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
train_y = keras.utils.to_categorical(train_y, 5)

# Check if there is a pre-trained model
if not os.path.exists('lstm_model.h5'):
    # Create a neural network with 3 dense layers
    model = Sequential()
    model.add(Embedding(3000, 64, input_length=300))
    model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(5, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(train_x, train_y, batch_size=32, epochs=10, verbose=1, validation_split=0.1, shuffle=True)

    # Save the model
    model.save('lstm_model.h5')
else:
    # Load the model from disk
    model = load_model('lstm_model.h5')

