# Import basic libraries and keras
import json
import numpy as np
from keras.models import load_model
from stories import get_stories, tokenize
from keras.preprocessing.sequence import pad_sequences

# Load test data
test_stories = get_stories('qa1_single-supporting-fact_test.txt')

# Load model, word index and lengths
model = load_model('rnn_model.h5')
with open('dictionary.json', 'r') as dictionary_file:
    word_idx = json.load(dictionary_file)
with open('lengths.json', 'r') as lengths_file:
    lengths = json.load(lengths_file)
    story_maxlen, query_maxlen = lengths["story_maxlen"], lengths["query_maxlen"]

# Get the word index of a question in a safe way
def best_effort_word_idxs(words):
    idxs = []
    for word in words:
        forms = [word, word.lower(), word[0].upper() + word[1:].lower()]
        for form in forms:
            if form in word_idx:
                idxs.append(word_idx[form])
    return idxs

while True:
    # Get a random story
    n = np.random.randint(0, 1000)
    story = test_stories[n][0]
    storystr = ' '.join(word for word in story)
    storymlstr = '\n'.join(storystr.split(' . '))[:-2]
    print(60 * '-')
    print('Story:\n' + storymlstr + '\n')

    # Request for a question
    print('Allowed vocabulary for questions:\n' + ' , '.join(word_idx.keys()))
    question = input('Enter your question (or press Enter to exit): ')
    if question == '':
        break

    # Tokenize story and question
    x = [word_idx[w] for w in story]
    xq = best_effort_word_idxs(tokenize(question)) #[word_idx[w] for w in tokenize(question)]
    if len(xq) < 1:
        print("Question is not valid")
        print(60 * '-')
        input("Press Enter to continue...\n")
        continue

    # Vectorize story and question
    tx, txq = pad_sequences([x], maxlen=story_maxlen), pad_sequences([xq], maxlen=query_maxlen)

    # Predict and print the result
    pred_results = model.predict(([tx, txq]))
    val_max = np.argmax(pred_results[0])
    for key, val in word_idx.items():
        if val == val_max:
            k = key
    print("Answer is: %s (confidence %.2f%%)" %(k, 100 * pred_results[0][val_max]))
    print(60 * '-')
    input("Press Enter to continue...\n")
