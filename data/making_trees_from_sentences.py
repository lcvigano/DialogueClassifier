# To run java server
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

from pycorenlp import StanfordCoreNLP
from nltk.tree import Tree
import re
import json
import ast
from tqdm import tqdm

def make_trees(data_file, person1, person2, train):
    print 'Creating trees...'
    f = open(data_file)
    if train:
        out_f = open(person1 + '_' + person2 + '_output_trees_training.txt', 'w')
    else:
        out_f = open(person1 + '_' + person2 + '_output_trees_testing.txt', 'w')

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
            tree = str(sentence['parse'])
            #now we have the tree, so write it
            out_f.write(person1)
            out_f.write('\n')
            out_f.write('*')
            out_f.write('\n')
            out_f.write(tree)
            out_f.write('\n')
            out_f.write('@')
            out_f.write('\n')

    person2_subtrees = {}
    print "Analyzing " + person2 + "'s Data..."
    for sentences in tqdm(person2_sentences):
        person2_output = nlp.annotate(sentences, properties={
          'annotators': 'parse',
          'outputFormat': 'json',
          })
        for sentence in person2_output['sentences']:
            tree = str(sentence['parse'])
            out_f.write(person2)
            out_f.write('\n')
            out_f.write('*')
            out_f.write('\n')
            out_f.write(tree)
            out_f.write('\n')
            out_f.write('@')
            out_f.write('\n')


    out_f.close()
