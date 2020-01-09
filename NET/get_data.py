from nltk.tree import Tree
import re
import subprocess
from pycorenlp import StanfordCoreNLP
import time
from tqdm import tqdm
import torch

nlp = StanfordCoreNLP('http://localhost:9000')

def write_sentence_file(names_trees_new):
    passive_active_file = open('../stanford-corenlp-full-2018-02-27/pa_sentence.txt', 'w')
    for pair in names_trees_new:
        tree = pair[1]
        sentence = str(tree.flatten()) # Strip to make into sentence
        sentence = re.sub('\(ROOT\s+', '', sentence)
        sentence = re.sub('\)', '', sentence)
        sentence = re.sub('\s+', ' ', sentence)
        sentence = re.sub("\s'", "'", sentence)
        passive_active_file.write(sentence + '\n')

    passive_active_file.close()

def passive_or_active(file_path):
    print 'Extracting Passive/Active features...'
    f = open(file_path)
    sentences = f.read().split('\n')[:-1]

    # Split data by speaker
    sentences_str = ['']
    curr_iter = 0
    for sentence in sentences:
        if any(ord(i)>127 for i in sentence):
            continue
        if len(sentences_str[curr_iter]) > 99000:
            curr_iter += 1
            sentences_str.append('')
        sentences_str[curr_iter] += ' ' + sentence

    features = []
    for sentence_set in tqdm(sentences_str):
        out = nlp.annotate(sentence_set, properties={
          'annotators': 'depparse',
          'outputFormat': 'json',
          })
        for sentence in out['sentences']:
            feature_set = False
            deps = sentence['basicDependencies']
            for dep in deps:
                if dep['dep'] == 'nsubjpass':
                    features.append(1)
                    feature_set = True
                    break
                elif dep['dep'] == 'nsubj':
                    features.append(-1)
                    feature_set = True
                    break
            if not feature_set:
                features.append(0)

    return features

def get_num_parses_in_thres(file_path):
    features = []
    print 'Extracting PCFG features (This may take awhile)...'
    proc = subprocess.Popen(['java', '-mx4g', '-cp', '../stanford-corenlp-full-2018-02-27/*', 'edu.stanford.nlp.parser.lexparser.LexicalizedParser', '-printPCFGkBest', '10', 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz', file_path],
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    parses = out.split('\n\n')
    parses = parses[:-1]
    scores = []
    for i in tqdm(range(len(parses))):
        if i == 0:
            continue
        parse = parses[i]
        if len(re.findall('[0-9]\n\(ROOT', parse)) == 0:
            best_score = scores[0]
            threshold = abs(best_score / 10.0)
            total = len(scores)
            scores = filter(lambda x: x > best_score - threshold and x < best_score + threshold, scores)
            features.append(len(scores) / float(total))
            scores = []
            continue
        else:
            score,tree_str = parse.split('\n', 1)
            tree = Tree.fromstring(tree_str)
            score = float(re.findall(r'-?[0-9]+.[0-9]+', score)[0])
            scores.append(score / len(tree.productions()))
    best_score = scores[0]
    threshold = abs(best_score / 10.0)
    total = len(scores)
    scores = filter(lambda x: x > best_score - threshold and x < best_score + threshold, scores)
    features.append(len(scores) / float(total))
    return features

def get_binaries(tree, person1, person2):
    # make a dictionary mapping the binaries to the character
    g=open('../data/' + person1 + '_' + person2 + '_binaries.txt')
    binary_list=[]
    for line in g.read().split('\n')[:-1]:
        if line==person1:
            char=line
            continue
        if line==person2:
            char=line
            continue
        binary_list.append((line,char))

    #binaries=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    binaries=[0 for x in range(binary_list)]
    for i in tree.subtrees():
        binaries_sub=[]
        x=re.sub('\s', '', re.sub(' [a-zA-Z0-9_.!?-]+\)', ')', str(i)))
        for j in range(len(binary_list)):
            if x==binary_list[j][0]:
                binaries_sub.append(1)
            else:
                binaries_sub.append(0)
        binaries=[sum(x) for x in zip(binaries, binaries_sub)]
    return binaries

def length_sentence(tree):
    return len(tree.pos())

def clause_length(tree):
    largest_clause_len=0
    for subtree in tree.subtrees():
        if subtree.label()=="SBAR":
            if length_sentence(subtree)>largest_clause_len:
                largest_clause_len=length_sentence(subtree)
    return largest_clause_len

def clause_height(tree):
    largest_clause_len=0
    for subtree in tree.subtrees():
        if subtree.label()=="SBAR":
            if height(subtree)>largest_clause_len:
                largest_clause_len=length_sentence(subtree)
    return largest_clause_len

def embedded_clause(tree):
    for subtree in tree.subtrees():
        if subtree.label()=="SBAR":
            return 1
    return 0

def height(tree):
    return tree.height()

# https://stackoverflow.com/questions/1833252/java-stanford-nlp-part-of-speech-labels
def noun_to_pronoun(tree):
    l = tree.pos()
    noun_count = 0
    pro_count = 0
    for tup in l:
        if tup[1] == 'NN' or tup[1] == 'NNS' or tup[1] == 'NNP' or tup[1] == 'NNPS':
            noun_count += 1
        if tup[1] == 'WP' or tup[1] == 'WP$' or tup[1] == 'PRP' or tup[1] == 'PRP$':
            pro_count += 1
    return noun_count - pro_count

def num_words_before_main_verb(tree):
    found_VP = False
    count = 0
    for s in tree.subtrees():
        if found_VP == False and s.label() == "VP":
            found_VP = True
            start_of_VP = s.flatten()[0]
    if not found_VP:
        return -1
    for word in tree.flatten():
        if word != start_of_VP:
            count += 1
        if word == start_of_VP:
            return count

def get_data(tree_path, person1, person2):
    f = open(tree_path)
    names_trees = f.read().split('@')
    names_trees_new=[]
    for s in names_trees:
        names_trees_new.append(s.split('*'))
    # now names_trees looks like [[person1,'tree for person1 as a string'],[person2, 'tree for person2 as a string']]
    names_trees_new=names_trees_new[:-1]
    for l in names_trees_new:
        tree = Tree.fromstring(l[1])
        l[1] = tree #overwrite it
        l[0] = l[0].strip('\n')

    features = []
    # extract fast features
    print 'Extracting initial features...'
    for sentence in tqdm(names_trees_new):
        nn_dict={}
        nn_dict['x']=get_binaries(sentence[1], person1, person2)+[height(sentence[1])]+[length_sentence(sentence[1])]+[noun_to_pronoun(sentence[1])]+[clause_length(sentence[1])]+[embedded_clause(sentence[1])]+[clause_height(sentence[1])]+[num_words_before_main_verb(sentence[1])]
        if sentence[0]==person1:
            nn_dict['y']= 0
        elif sentence[0]==person2:
            nn_dict['y']= 1
        nn_dict['tree']=sentence[1]
        features.append(nn_dict)

    # extract PCFG and passive/active features
    write_sentence_file(names_trees_new)
    num_parse_feat = get_num_parses_in_thres('../stanford-corenlp-full-2018-02-27/pa_sentence.txt')
    passive_active_feat = passive_or_active('../stanford-corenlp-full-2018-02-27/pa_sentence.txt')
    for i in range(len(features)):
        features[i]['x'] += [num_parse_feat[i]]
        features[i]['x'] += [passive_active_feat[i]]
        features[i]['x'] = torch.FloatTensor(features[i]['x'])
    print len(features)
    return features