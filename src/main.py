from Parser import Parser
from CKY import CKY

def readDocument(path):
    file = open(path, 'r+')

    SentenceParser = Parser()
    parse_information = SentenceParser.load_database( 'parse_information.p' )

    Algorithm = CKY( parse_information )

    for sentence in file:
        parse = Algorithm.run( sentence )
        print sentence
        print parse
        print '======'

if __name__ == '__main__':
    readDocument('../data/test.sentence.23')
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
