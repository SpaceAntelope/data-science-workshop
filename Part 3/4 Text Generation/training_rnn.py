# Import basic libraries and keras
import os
import json
from keras import layers
from keras.layers import LSTM
from keras.models import Model
from keras.models import load_model
from stories import get_stories, vectorize_stories

# Set parameters
EMBED_HIDDEN_SIZE = 50
SENT_HIDDEN_SIZE = 100
QUERY_HIDDEN_SIZE = 100
BATCH_SIZE = 32
EPOCHS = 40

# Load input data
train = get_stories('qa1_single-supporting-fact_train.txt')
test = get_stories('qa1_single-supporting-fact_test.txt')

# Create vocabulary
vocab = set()
for story, q, answer in train + test:
    vocab |= set(story + q + [answer])
vocab = sorted(vocab)

# Create index of words {word: id}
# Reserve 0 for masking via pad_sequences
vocab_size = len(vocab) + 1
word_idx = dict((c, i + 1) for i, c in enumerate(vocab))
# Get maximum length of sequences
story_maxlen = max(map(len, (x for x, _, _ in train + test)))
query_maxlen = max(map(len, (x for _, x, _ in train + test)))

# Save vocabulary and lengths to file
if not os.path.exists('dictionary.json'):
    with open('dictionary.json', 'w') as outfile:
        json.dump(word_idx, outfile)
if not os.path.exists('lengths.json'):
    with open('lengths.json', 'w') as outfile:
        json.dump({'story_maxlen': story_maxlen, 'query_maxlen': query_maxlen}, outfile)

# Vectorize the stories
x, xq, y = vectorize_stories(train, word_idx, story_maxlen, query_maxlen)
tx, txq, ty = vectorize_stories(test, word_idx, story_maxlen, query_maxlen)

# Check if there is a pre-trained model
if not os.path.exists('rnn_model.h5'):
    # Create a neural network for the stories
    sentence = layers.Input(shape=(story_maxlen,), dtype='int32')
    encoded_sentence = layers.Embedding(vocab_size, EMBED_HIDDEN_SIZE)(sentence)
    encoded_sentence = layers.Dropout(0.3)(encoded_sentence)
    
    # Create a neural network for the questions
    question = layers.Input(shape=(query_maxlen,), dtype='int32')
    encoded_question = layers.Embedding(vocab_size, EMBED_HIDDEN_SIZE)(question)
    encoded_question = layers.Dropout(0.3)(encoded_question)
    encoded_question = LSTM(EMBED_HIDDEN_SIZE)(encoded_question)
    encoded_question = layers.RepeatVector(story_maxlen)(encoded_question)
    
    # Combine the two networks
    merged = layers.add([encoded_sentence, encoded_question])
    merged = LSTM(EMBED_HIDDEN_SIZE)(merged)
    merged = layers.Dropout(0.3)(merged)
    preds = layers.Dense(vocab_size, activation='softmax')(merged)
    model = Model([sentence, question], preds)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Train the model
    model.fit([x, xq], y, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.05)
    
    # Save the model
    model.save('rnn_model.h5')
else:
    # Load the model from disk
    model = load_model('rnn_model.h5')

model.summary()
score = model.evaluate([tx, txq], ty, batch_size=BATCH_SIZE, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

