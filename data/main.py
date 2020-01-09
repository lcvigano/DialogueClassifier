import argparse
from making_trees_from_sentences import make_trees
from pattern_finder import find_patterns
from pattern_extracter import extract_patterns

parser = argparse.ArgumentParser(description='6.863 Final Project')

parser.add_argument('--person1', type=str, required=True, help='name of person1 as listed in the data files')
parser.add_argument('--person2', type=str, required=True, help='name of person2 as listed in the data files')
parser.add_argument('--train_file', type=str, required=True, help='training file name')
parser.add_argument('--test_file', type=str, required=True, help='test file name')

args = parser.parse_args()

if __name__ == '__main__':
    # Create training data and binaries
    print 'Training Data:'
    make_trees(args.train_file, args.person1, args.person2, train=True)
    find_patterns(args.train_file, args.person1, args.person2)
    extract_patterns(args.person1, args.person2)

    print '\n\nTesting Data:'
    # Create testing data
    make_trees(args.test_file, args.person1, args.person2, train=False)