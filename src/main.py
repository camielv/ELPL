from Parser import Parser
from CKY import CKY
import operator
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

def readDocument(path_sentences, path_trees):
    file_sentences = open(path_sentences, 'r+')
    file_trees     = open(path_trees, 'r+')
    correct_trees  = open("set_correct2.txt", 'w+')
    test_trees  = open("set_test2.txt", 'w+')

    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information_unknown.p' )
    Algorithm = CKY( parse_information )

    i = 0
    correct = 0
    total = 0
    while True:
        sentence     = file_sentences.readline()
        correct_tree = file_trees.readline()
        words = sentence.split(' ')

        size = len(words) - 2
        print "Sentence:", i, "Size:", size
        if i < 748+833:
            i += 1
            continue
        i += 1
        if sentence == '':
            break
#        if(size > 20):
#            continue
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
    TreeParser.save_database(database, 'parse_information_unknown.p')

if __name__ == '__main__':
    #parseData()
    printStep2()
    #readDocument('../data/test.sentence.23', '../data/test.trees.23')
    #printKeys()
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
