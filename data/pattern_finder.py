# To run java server
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

# NLTK Tree Class
# https://www.nltk.org/_modules/nltk/tree.html#Tree

from pycorenlp import StanfordCoreNLP
from nltk.tree import Tree
import re
import json
import ast
from tqdm import tqdm

def find_patterns(data_file, person1, person2):
    print '\nFinding syntactic patterns...'
    # Extract data from txt file
    f = open(data_file)
    speaker_sentence_pairs = f.read().split('\n')[:-1]

    # Split data by speaker
    person1_sentences = ['']
    person2_sentences = ['']

    curr_iter_person1 = 0
    curr_iter_person2 = 0

    for sentence in speaker_sentence_pairs:
        speaker,dialogue = sentence.split('|')
        if any(ord(i)>127 for i in dialogue):
            continue
        if len(person1_sentences[curr_iter_person1]) > 99000:
            curr_iter_person1 += 1
            person1_sentences.append('')
        if len(person2_sentences[curr_iter_person2]) > 99000:
            curr_iter_person2 += 1
            person2_sentences.append('')
        if speaker == person1:
            person1_sentences[curr_iter_person1] += ' ' + dialogue
        elif speaker == person2:
            person2_sentences[curr_iter_person2] += ' ' + dialogue

    # Run data through parser and aggregate data
    person1_subtrees = {}
    print "Analyzing " + person1 + "'s Data..."
    for sentences in tqdm(person1_sentences):
        nlp = StanfordCoreNLP('http://localhost:9000')
        person1_output = nlp.annotate(sentences, properties={
          'annotators': 'parse',
          'outputFormat': 'json',
          })
        for sentence in person1_output['sentences']:
            for tree in Tree.fromstring(sentence['parse']).subtrees():
                tree_str = re.sub('\s', '', re.sub(' [a-zA-Z0-9_.!?-]+\)', ')', str(tree)))
                if tree_str in person1_subtrees:
                    person1_subtrees[tree_str] += 1
                else:
                    person1_subtrees[tree_str] = 1

    person2_subtrees = {}
    print "Analyzing " + person2 + "'s Data..."
    for sentences in tqdm(person2_sentences):
        person2_output = nlp.annotate(sentences, properties={
          'annotators': 'parse',
          'outputFormat': 'json',
          })
        for sentence in person2_output['sentences']:
            for tree in Tree.fromstring(sentence['parse']).subtrees():
                tree_str = re.sub('\s', '', re.sub(' [a-zA-Z0-9_.!?-]+\)', ')', str(tree)))
                if tree_str in person2_subtrees:
                    person2_subtrees[tree_str] += 1
                else:
                    person2_subtrees[tree_str] = 1

    print 'Sorting data...'
    person1_sorted_strs = sorted(person1_subtrees.keys(), key=lambda x: person1_subtrees[x], reverse=True)
    person2_sorted_strs = sorted(person2_subtrees.keys(), key=lambda x: person2_subtrees[x], reverse=True)

    print 'Writing data...'
    with open(person1 + '_sorted_result.out', 'w') as fp:
        for tree_str in person1_sorted_strs:
            fp.write(tree_str + ' | ' + str(person1_subtrees[tree_str]) + '\n')

    with open(person2 + '_sorted_result.out', 'w') as fp:
        for tree_str in person2_sorted_strs:
            fp.write(tree_str + ' | ' + str(person2_subtrees[tree_str]) + '\n')
