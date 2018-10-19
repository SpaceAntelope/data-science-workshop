import os

def load_data(data_path = 'bbc'):
    classes = ['business', 'entertainment', 'politics', 'sport', 'tech']
    texts = []
    labels = []
    for i, aclass in enumerate(classes):
        path = os.path.join(data_path, aclass)
        for atext in os.listdir(path):
            with open(os.path.join(path, atext)) as infile:
                data = infile.readlines()
                texts.append(data[0])
                labels.append(i)
    return texts, labels

