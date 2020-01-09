import argparse
import torch
from net import Net
from train import train_model
from test import test_model
from get_data import get_data

parser = argparse.ArgumentParser(description='6.863 Final Project')

parser.add_argument('--person1', type=str, required=True, help='name of person1 as listed in the data files')
parser.add_argument('--person2', type=str, required=True, help='name of person2 as listed in the data files')

parser.add_argument('--train', action='store_true', default=False, help='train lstm')
parser.add_argument('--test', action='store_true', default=False, help='test lstm')
parser.add_argument('--model_file', type=str, default="", help='filename')

parser.add_argument('--lr', type=float, default=0.001, help='initial learning rate [default: 0.001]')
parser.add_argument('--wd', type=float, default=0.0, help='initial weight decay [default: 0.0]')
parser.add_argument('--epochs', type=int, default=50, help='number of epochs for train [default: 50]')
parser.add_argument('--batch_size', type=int, default=16, help='batch size for training [default: 16]')
parser.add_argument('--num_workers', nargs='?', type=int, default=4, help='num workers for data loader')

args = parser.parse_args()

if __name__ == '__main__':
    if args.train:
        train_data = get_data('../data/' + args.person1 + '_' + args.person2 + '_output_trees_training.txt', args.person1, args.person2)
        if args.model_file:
            model = torch.load(args.model_file)
        else:
            model = Net(len(train_data[0]['x']))
        model = train_model(train_data, model, args)

    if args.test:
        test_data = get_data('../data/' + args.person1 + '_' + args.person2 + '_output_trees_testing.txt', args.person1, args.person2)
        if args.model_file:
            model = torch.load(args.model_file)
            print "Test results:"
            test_model(test_data, model)
        else:
            print "Model file required to evaluate."