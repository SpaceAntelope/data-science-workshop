# Import basic libraries and keras
import json
from keras.models import load_model
from keras.preprocessing.text import Tokenizer, text_to_word_sequence

# Load the dictionary and the model
with open('dictionary.json', 'r') as dictionary_file:
    dictionary = json.load(dictionary_file)
model = load_model('model.h5')

tokenizer = Tokenizer(num_words=3000)
while 1:
    text = input('Input a sentence to evaluate its sentiment, or press enter to quit: ')
    if len(text) == 0:
        break
    # Make the prediction
    words = text_to_word_sequence(text)
    wordIndices = [dictionary[word] for word in words if word in dictionary]
    testdata = tokenizer.sequences_to_matrix([wordIndices], mode='binary')
    pred = model.predict(testdata)[0]
    print("The sentiment is %s (confidence: %.2f%%)" % ("negative" if pred[0] > pred[1] else "positive", 100 * max(pred)))
