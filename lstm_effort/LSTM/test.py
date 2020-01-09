import torch
import torch.autograd as autograd
import torch.nn.functional as F
import torch.utils.data as data
from tqdm import tqdm
import numpy as np

torch.manual_seed(1)

def test_lstm(test_data, model, args):

    data_loader = torch.utils.data.DataLoader(
        test_data,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        drop_last=True)

    print 'Testing model...'

    total = 0.0
    correct = 0.0
    for batch in tqdm(data_loader):

        x, y = autograd.Variable(batch['x']), autograd.Variable(batch['y'])
        out = model(x)
        out = F.log_softmax(out)

        for i in range(args.batch_size):
            prediction = np.argmax(out[i].data.cpu().numpy())
            ground_truth = y[i].data.cpu().numpy()[0]
            if prediction == ground_truth:
                correct += 1.0
            total += 1.0

    print 'Accuracy: ' + str(correct/total)
    return model