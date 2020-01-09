import torch
import torch.autograd as autograd
import torch.nn.functional as F
import torch.utils.data as data
from tqdm import tqdm
import numpy as np

torch.manual_seed(1)

def train_model(train_data, model, args):

    optimizer = torch.optim.Adam(model.parameters() , lr=args.lr, weight_decay=args.wd)

    model.train()

    for epoch in range(1, args.epochs+1):

        print("-------------\nEpoch {}:\n".format(epoch))

        loss = run_epoch(train_data, True, model, optimizer, args)

        print('Train NLL loss: {:.6f}'.format( loss))

        # Save model
        torch.save(model, 'model_lr_' + str(args.lr)[0:6] + '_wd_' +
                            str(args.wd)[0:6] + '_epoch_' + str(epoch) + '.pt')

    return model

def run_epoch(data, is_training, model, optimizer, args):
    '''
    Train model for one pass of train data, and return loss, acccuracy
    '''
    data_loader = torch.utils.data.DataLoader(
        data,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        drop_last=True)

    losses = []

    if is_training:
        model.train()
    else:
        model.eval()

    for batch in tqdm(data_loader):

        x, y = autograd.Variable(batch['x']), autograd.Variable(batch['y'])

        if is_training:
            optimizer.zero_grad()

        out = model(x)

        loss = F.nll_loss(out, y.long())

        if is_training:
            loss.backward()
            optimizer.step()

        losses.append(loss.cpu().data[0])

    # Calculate epoch level scores
    avg_loss = np.mean(losses)
    return avg_loss