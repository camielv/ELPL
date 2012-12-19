from Parser import Parser
from CKY import CKY
import operator
import argparse
import time

def readDocument(path_sentences, path_trees):
    file_sentences = open(path_sentences, 'r+')
    file_trees     = open(path_trees, 'r+')
    correct_trees  = open("GOLD_OUTPUT_" + str(time.time()) + ".txt", 'w+')
    test_trees  = open("TEST_OUTPUT_" + str(time.time()) + ".txt", 'w+')

    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information_unknown.p' )
    Algorithm = CKY( parse_information )

    i = 0
    while True:
        sentence     = file_sentences.readline()
        correct_tree = file_trees.readline()
        words = sentence.split(' ')

        size = len(words) - 2
        print "Sentence:", i, "Size:", size
        i += 1
        if sentence == '':
            break

        # Run CKY and Viterbi
        tree = Algorithm.run( words[:size] )
        if tree:
            test_trees.write(tree)
            correct_trees.write(correct_tree)

    correct_trees.close()
    test_trees.close()

def parseData(path_corpus):
    TreeParser = Parser()
    database = TreeParser.parse_document(path_corpus)
    TreeParser.save_database(database, 'parse_information_unknown.p')

if __name__ == '__main__':
    inputParser = argparse.ArgumentParser(description='CKY and Viterbi implementation by Anna Keune (6056547) and Camiel Verschoor (6229298)')
    info = {
    'c' : 'Path of the training corpus file.',
    's' : 'Path of the test sentences.',
    't' : 'Path of the test trees (golden standard file).',
    }
    
    # Required parameters
    inputParser.add_argument('-c', '--corpus-path', type=str, help=info['c'], required=True)
    inputParser.add_argument('-s', '--sentences-path', type=str, help=info['s'], required=True)
    inputParser.add_argument('-t', '--test-trees-path', type=str, help=info['t'], required=True)
    
    # Optional parameters
    inputparser.add_argument('-l', '--max-sentence-length', type=int, default=15, help=info['l'])   
    
    
    arguments = inputParser.parse_args()
    
    parseData(arguments.corpus_path)
    readDocument(arguments.sentences_path, arguments.test_trees_path)





'''
####################################################
# GARBAGE CODE USED TO PRINT SEVERAL PROBABILITIES #
####################################################
def printKeys():
    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information_unknown.p' )
    print parse_information['transition_terminal'].keys()


def printStep2():
    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information_unknown.p' )
    category = ['VP', 'S', 'NP', 'SBAR', 'PP']
    for key in category:
        possible  = parse_information['probability_non-terminal'][key]
        sorted_dict = sorted(possible.iteritems(), key=operator.itemgetter(1), reverse=True)
        for i in range(4):
            print key, "->", sorted_dict[i], 'P', sorted_dict[i][1] / float(sum(possible.values()))

def printStep1():
    best = 0
    best_key = None
    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information_unknown.p' )
    for key in parse_information['transition_terminal']:
        if len(parse_information['transition_terminal'][key]) > 3:
            rules = parse_information['transition_terminal'][key]
            count = sum(parse_information['transition_terminal'][key].values())
            if count > best and count != 47976 and count != 28597 and count !=22242 and count!= 20149:
                best = count
                best_key = key
            for rule in rules:
                P = parse_information['probability_terminal'][rule][key] / float(sum(parse_information['probability_terminal'][rule].values()))
                print rule, "->", key, ":", P
    print best, best_key
    rules = parse_information['transition_terminal'][best_key]
    for rule in rules:
        total_count = parse_information['probability_terminal'][rule].values()
        if (rule,) in parse_information['probability_non-terminal']:
            total_count += parse_information['probability_non-terminal'][(rule,)].values()
        P = parse_information['probability_terminal'][rule][best_key] / float(sum(total_count))
        print rule, "->", best_key, ":", P
'''
