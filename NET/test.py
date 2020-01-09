import torch
import torch.autograd as autograd
from tqdm import tqdm
import numpy as np

torch.manual_seed(1)

def test_model(test_data, model):

    print 'Testing model...'

    total = 0.0
    correct = 0.0
    for i in tqdm(range(len(test_data))):
        sentence = test_data[i]
        x, y = autograd.Variable(sentence['x']), autograd.Variable(torch.FloatTensor([sentence['y']]))
        out = model(x)
        prediction = np.argmax(out.data.cpu().numpy())
        ground_truth = y.data.cpu().numpy()[0]
        if prediction == ground_truth:
            correct += 1.0
        total += 1.0

    print 'Accuracy: ' + str(correct/total)
    return model