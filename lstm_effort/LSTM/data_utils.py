import gzip
import numpy as np
import torch
import cPickle as pickle
import full_simpsons_dataset as dataset

# Load word vector embeddings
def getEmbeddingTensor():
    embedding_path='../data/vectors.txt.gz'
    lines = []
    with gzip.open(embedding_path) as file:
        lines = file.readlines()
        file.close()
    embedding_tensor = []
    word_to_indx = {}
    for indx, l in enumerate(lines):
        word, emb = l.split()[0], l.split()[1:]
        vector = [float(x) for x in emb ]
        if indx == 0:
            embedding_tensor.append( np.zeros( len(vector) ) )
        embedding_tensor.append(vector)
        word_to_indx[word] = indx+1
    embedding_tensor = np.array(embedding_tensor, dtype=np.float32)


    return embedding_tensor, word_to_indx


def load_dataset(label_map):
    print "\nLoading data..."
    embeddings, word_to_indx = getEmbeddingTensor()

    train_data = dataset.FullSimpsonsDataset('../data/training_data.txt', word_to_indx, label_map)
    test_data = dataset.FullSimpsonsDataset('../data/testing_data.txt', word_to_indx, label_map)

    return train_data, test_data, embeddings

















