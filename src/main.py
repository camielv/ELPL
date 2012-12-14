from Parser import Parser
from CKY import CKY
import re

def readDocument(path_sentences, path_trees):
    file_sentences = open(path_sentences, 'r+')
    file_trees     = open(path_trees, 'r+')

    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information.p' )
    Algorithm = CKY( parse_information )

    i = 0
    correct = 0
    total = 0
    while True:
        sentence = file_sentences.readline()
        correct_tree = file_trees.readline()
        n = len(sentence)
        words = sentence[0:n-3].split( ' ' )
        size = len(words)
        print "Sentence:", i, "Size:", size
        if sentence == '':
            break
        if(size > 20):
            i += 1
            continue
        i += 1
        total += 1

        tree = Algorithm.run( words )
        #print tree
        if tree == correct_tree:
            correct += 1
            print correct_tree

    print correct, total
    print correct / float(total)

if __name__ == '__main__':
    readDocument('../data/test.sentence.23', '../data/test.trees.23')
    '''
    x = Parser()
    #parse_information = x.parse_document( '../data/wsj.02-21.training.nounary' )
    #x.save_database( parse_information, 'parse_information.p' )
    parse_information = x.load_database( 'parse_information.p' )
    sentence = '`` The equity market was illiquid .'
    test_s   = 'Not all those who wrote oppose the changes .'
    y = CKY( parse_information )
    best_parse = y.run( test_s )
    print best_parse
    '''
    '''
    keys = parse_information['probability_non-terminal'].keys()
    i = 0
    for key in keys:
        if i == 10:
            break
        print key, parse_information['probability_non-terminal'][key]
        i+= 1
    i = 0
    keys = parse_information['transition_non-terminal'].keys()
    for key in keys:
        if i == 10:
            break
        print key, parse_information['transition_non-terminal'][key]
        i+=1
    '''
    #y = CKY( parse_information )
    #best_parse = y.run( sentence )
