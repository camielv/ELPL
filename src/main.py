from Parser import Parser
from CKY import CKY
def printStep1():
    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information.p' )
    for key in parse_information['transition_terminal']:
        if len(parse_information['transition_terminal'][key]) > 3:
            rules = parse_information['transition_terminal'][key]
            for rule in rules:
                P = parse_information['probability_terminal'][rule][key] / float(sum(parse_information['probability_terminal'][rule].values()))
                print rule, "->", key, ":", P
    

def readDocument(path_sentences, path_trees):
    file_sentences = open(path_sentences, 'r+')
    file_trees     = open(path_trees, 'r+')
    correct_trees  = open("correct.txt", 'w+')
    test_trees  = open("test.txt", 'w+')

    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information15.p' )
    Algorithm = CKY( parse_information )

    i = 0
    correct = 0
    total = 0
    while True:
        sentence     = file_sentences.readline().upper()
        correct_tree = file_trees.readline().upper()
        words = sentence.split( ' ' )

        size = len(words) - 2
        print "Sentence:", i, "Size:", size
        i += 1
        if sentence == '':
            break
        if(size > 10):
            continue
        # Total actual parsed sentences
        total += 1

        # Run CKY and Viterbi
        tree = Algorithm.run( words[:size] )
        if tree:
            test_trees.write(tree)
            correct_trees.write(correct_tree)

    correct_trees.close()
    test_trees.close()

def parseData():
    TreeParser = Parser()
    database = TreeParser.parse_document('../data/wsj.02-21.training.nounary')
    TreeParser.save_database(database, 'parse_information15.p')


if __name__ == '__main__':
    #parseData()
    #printStep1()
    readDocument('../data/test.sentence.23', '../data/test.trees.23')
    '''
    x = Parser()
    #x.save_database( parse_information, 'parse_information15.p' )
    #sentence = '`` The equity market was illiquid .'
    #test_s   = 'Not all those who wrote oppose the changes .'
    #y = CKY( parse_information )
    #best_parse = y.run( test_s )
    #print best_parse
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
