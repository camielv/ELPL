import cPickle as pickle
import operator
'''
    We save the rules in a in dictionary of dictionaries as dictionaries are a quick datatype.
'''
class Parser():
    def __init__(self):
        pass

    def save_database(self, database, path):
        ''' Saves a database of dicts '''
        pickle.dump( database, open( path, 'wb' ) )

    def load_database(self, path):
        ''' Loads a database of dicts '''
        return pickle.load( open( path, 'rb' ) )

    def parse_document(self, path):
        ''' Parses a document of annotated sentences '''
        file = open( path, 'r+' )
        parse_information = dict()
        parse_information['probability_terminal']     = dict()
        parse_information['probability_non-terminal'] = dict()
        parse_information['transition_terminal']      = dict()
        parse_information['transition_non-terminal']  = dict()

        for sentence in file:
            parse_information = self.parse_sentence(sentence, parse_information)

        return parse_information

    def parse_sentence(self, sentence, parse_information):
        ''' Parses a annotated sentence linearly for probabilty of a transition and a transition '''
        count = sentence.count( '(' )
        if count  == 0:
            print 'Error: Non-valid sentence!'
            return database, probability

        # Temporary datastructure to save nodes.
        temp_db  = dict()
        length = len( sentence )
        depth = 0
        iterator = sentence.find( '(' )
        # If the current parenthesis is open (True) or closed (False)
        iterator_status = True

        while( depth >= 0 ):
            # Find next closest parenthesis.
            left_pos  = sentence.find( '(', iterator+1 )
            right_pos = sentence.find( ')', iterator+1 )

            # Determine what parenthesis is closer.
            if left_pos < right_pos and left_pos != -1:
                # Case if previous parenthesis is open and current is open.
                if iterator_status:
                    # Save it to the temporary database
                    if depth in temp_db:
                        temp_db[depth].append( sentence[iterator+1:left_pos-1] )
                    else:
                        temp_db[depth] = [ sentence[iterator+1:left_pos-1] ]

                # Case if previous parenthesis is closed and current is open
                else:
                    pass
                depth += 1
                iterator = left_pos
                iterator_status = True
            else:
                # Case if previous parenthesis is open and current is closed.
                if iterator_status:
                    # Terminal case, extract terminal.
                    temp  = sentence[iterator+1:right_pos]
                    terms = temp.split( ' ' )

                    # Update probability database
                    if terms[0] in parse_information['probability_terminal']:
                        if terms[1] in parse_information['probability_terminal'][terms[0]]:
                            parse_information['probability_terminal'][terms[0]][terms[1]] += 1
                        else:
                            parse_information['probability_terminal'][terms[0]][terms[1]] = 1
                    else:
                        parse_information['probability_terminal'][terms[0]] = {terms[1]: 1}

                    # Update transition database
                    if terms[1] in parse_information['transition_terminal']:
                        if terms[0] in parse_information['transition_terminal'][terms[1]]:
                            pass
                        else:
                            parse_information['transition_terminal'][terms[1]].append( terms[0] )
                    else:
                        parse_information['transition_terminal'][terms[1]] = [terms[0]]

                    # Saving for higher depth
                    if depth in temp_db:
                        temp_db[depth].append( terms[0] )
                    else:
                        temp_db[depth] = [ terms[0] ]

                # Case if previous parenthesis is closed and current is closed.
                else:
                    left_term = temp_db[depth][len(temp_db[depth])-1]
                    right_term = tuple(temp_db[depth+1])

                    # Update probability database
                    if left_term in parse_information['probability_non-terminal']:
                        if right_term in parse_information['probability_non-terminal'][left_term]:
                            parse_information['probability_non-terminal'][left_term][right_term] += 1
                        else:
                            parse_information['probability_non-terminal'][left_term][right_term] = 1
                    else:
                        parse_information['probability_non-terminal'][left_term] = {right_term: 1}

                    # Update transition database
                    if right_term in parse_information['transition_non-terminal']:
                        if left_term in parse_information['transition_non-terminal'][right_term]:
                            pass
                        else:
                            parse_information['transition_non-terminal'][right_term].append( left_term )
                    else:
                        parse_information['transition_non-terminal'][right_term] = [left_term]

                    del temp_db[depth+1] 
                depth -= 1
                iterator = right_pos
                iterator_status = False
        return parse_information

class CKY():
    def __init__( self, parse_information):
        self.parse_information = parse_information
        self.score = dict()
        self.trace = dict()

    def run( self, sentence ):
        # Split the sentence
        words = sentence.split( ' ' )
        n     = len( words )

        # Create table
        score = dict()
        trace = dict()
        for i in range(n+1):
            for j in range(n+1):
                score[(i,j)] = dict()
                trace[(i,j)] = dict()

        # Step 1 search terminal possibilities and save them with probability
        for i in range(n):
            # Check if terminal exists
            if words[i] in parse_information['transition_terminal']:
                # Find all possible rules to terminal and save them
                poss_rules = parse_information['transition_terminal'][ words[i] ]
                for rule in poss_rules:
                    key = (rule,)
#                    print 'New Rule Found:', rule, '->', words[i]
                    score[(i, i+1)][ key ] = \
                        parse_information['probability_terminal'][ rule ][ words[i] ] / \
                        float( sum( parse_information['probability_terminal'][ rule ].values() ) )
                    trace[(i, i+1)][ key ] = words[i]

        # Step 2 handle unaries
                added = True
                while added:
                    added = False
                    # Look for possible candidates for unary and find their
                    # corresponding transition
                    candidates = score[(i, i+1)].keys()
                    for candidate in candidates:
                        if candidate in parse_information['transition_non-terminal']:
                            poss_unaries = parse_information['transition_non-terminal'][ candidate ]
                            for unary in poss_unaries:
                                P = ( parse_information['probability_non-terminal'][ unary ][ candidate ] / \
                                    float( sum( parse_information['probability_non-terminal'][ unary ].values() ) ) ) * \
                                    score[(i, i+1)][ candidate ]
                                # When the corresponding transition does not exist or has a higher probability save it
                                unary = (unary,)
                                if not( unary in score[(i, i+1)] ):
#                                    print 'New Unary Found:', unary, '->', candidate
                                    score[(i, i+1)][ unary ] = P
                                    trace[(i, i+1)][ unary ] = candidate
                                    added = True
                                elif P > score[(i, i+1)][unary]:
#                                    print 'Better Unary Found:', unary, '->', candidate
#                                    print 'New:', P, 'Previous:', score[(i, i+1)][unary]
                                    score[(i, i+1)][ unary ] = P
                                    trace[(i, i+1)][ unary ] = candidate
                                    added = True
            else:
                print "Terminal does not exist in database"
                return False
        # Step 3 binaries
        # Loop diagonally over the table
        for span in range(2, n+1):
            for begin in range((n - span)+1):
                end = begin + span
                for split in range(begin+1, end):
                    candidates_A = score[(begin, split)].keys()
                    candidates_B = score[(split, end)].keys()
                    for candidate_A in candidates_A:
                        for candidate_B in candidates_B:
                            consequence = (candidate_A[0], candidate_B[0])
                            if consequence in parse_information['transition_non-terminal']:
                                poss_rules = parse_information['transition_non-terminal'][consequence]
                                for poss_rule in poss_rules:
                                    P = score[(begin, split)][candidate_A] * \
                                        score[(split, end)][candidate_B] * \
                                        parse_information['probability_non-terminal'][poss_rule][consequence] / \
                                        float(sum(parse_information['probability_non-terminal'][ poss_rule ].values() ) )
                                    poss_rule = (poss_rule,)
                                    if not( poss_rule in score[(begin, end)] ):
#                                        print 'New Rule Found:', poss_rule, '->', consequence
                                        score[(begin, end)][poss_rule] = P
                                        trace[(begin, end)][poss_rule] = (consequence, split)

                                    elif P > score[(begin, end)][ poss_rule ]:
#                                        print 'Better Rule Found:', poss_rule, '->', consequence
#                                        print 'New:', P, 'Previous:', score[(begin, end)][poss_rule]
                                        score[(begin, end)][poss_rule] = P
                                        trace[(begin, end)][poss_rule] = (consequence, split)
        # Step 4 unaries
                added = True
                while added:
                    added = False
                    candidates = score[(begin, end)].keys()
                    # All possible rules for a unary
                    for candidate in candidates:
                        if candidate in parse_information['transition_non-terminal']:
                            poss_unaries = parse_information['transition_non-terminal'][ candidate ]
                            for unary in poss_unaries:
                                P = ( parse_information['probability_non-terminal'][ unary ][ candidate ] / \
                                    float( sum( parse_information['probability_non-terminal'][ unary ].values() ) ) ) * \
                                    score[(begin, end)][candidate]
                                unary = (unary,)
                                if not( unary in score[(begin, end)] ):
#                                    print 'New Unary Found:', unary, '->', candidate
                                    score[(begin, end)][unary] = P
                                    trace[(begin, end)][unary] = candidate
                                    added = True
                                elif P > score[(begin, end)][ unary ]:
#                                    print 'Better Unary Found:', unary, '->', candidate
#                                    print 'New:', P, 'Previous:', score[(begin, end)][unary]
                                    score[(begin, end)][unary] = P
                                    trace[(begin, end)][unary] = candidate
                                    added = True
        self.score = score
        self.trace = trace
        return self.viterbi(0, n, ('TOP',))

    def viterbi(self, i, j, tag):
        print "========"
        if(abs(i-j) == 1):
            if isinstance(tag, str):
                print i, j, tag
                return tag
            else:
                print i, j, tag[0]
                rule = self.trace[(i,j)][tag]
                return tag[0], self.viterbi(i, j, rule)
        best = self.score[(i,j)][tag]
        print i, j, tag[0]
        print self.score[(i,j)]
        rule = self.trace[(i,j)][tag]
        print best, rule
        if len(rule) == 1:
            return tag[0], self.viterbi(i, j, rule)
        else:
            x = self.viterbi(i, rule[1], (rule[0][0],))
            y = self.viterbi(rule[1], j, (rule[0][1],))
            # NP@ check. Remove NP@
            if tag[0].count('@') > 0:
                return x, y
            elif tag[0].count('%') > 0 and tag[0].count('%') % 5 == 0:
                pass
                print "PERCENT ALERT", tag[0]
                pos_tags = tuple(tag[0].split('%%%%%'))
                count_tags = len(pos_tags)
                test = (pos_tags[count_tags-1], x, y)
                for i in range(len(pos_tags)-2,0-1,-1):
                    test = (pos_tags[i], test)
                return test
            if isinstance(x[0], tuple) and isinstance(y[0], tuple):
                return tag[0], x[0], x[1], y[0], y[1]
            elif isinstance(x[0], tuple):
                return tag[0], x[0], x[1], y
            elif isinstance(y[0], tuple):
                return tag[0], x, y[0], y[1]
                    
            return tag[0], x, y
       
        

if __name__ == '__main__':
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
