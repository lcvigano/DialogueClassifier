import argparse
import data_utils
from train import train_model
from lstm import LSTM
from test import test_lstm
import torch

parser = argparse.ArgumentParser(description='6.806 Final Project')

parser.add_argument('--train', action='store_true', default=False, help='train lstm')
parser.add_argument('--test', action='store_true', default=False, help='test lstm')
parser.add_argument('--model_file', type=str, default="", help='filename')

parser.add_argument('--lr', type=float, default=0.001, help='initial learning rate [default: 0.001]')
parser.add_argument('--wd', type=float, default=0.0, help='initial weight decay [default: 0.0]')
parser.add_argument('--epochs', type=int, default=50, help='number of epochs for train [default: 50]')
parser.add_argument('--batch_size', type=int, default=16, help='batch size for training [default: 16]')
parser.add_argument('--hidden_dim', type=int, default=150, help='hidden layer dimension size [default: 200]')
parser.add_argument('--num_workers', nargs='?', type=int, default=4, help='num workers for data loader')

args = parser.parse_args()

if __name__ == '__main__':

    label_map = {'bart simpson': 0, 'marge simpson': 1}
    train_data, test_data, embeddings = data_utils.load_dataset(label_map)

    if args.train:
        if args.model_file:
            model = torch.load(args.model_file)
        else:
            model = LSTM(embeddings, args)
        model = train_model(train_data, test_data, model, args)

    if args.test:
        if args.model_file:
            model = torch.load(args.model_file)
            print "Test results:"
            test_lstm(test_data, model, args)
        else:
            print "Model file required to evaluate question similarity."