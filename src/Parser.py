import cPickle as pickle
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
        probability = dict()
        transition  = dict()

        for sentence in file:
            probability, transition = self.parse_sentence( sentence, probability, transition )

        return probability, transition

    def parse_sentence(self, sentence, probability, transition):
        ''' Parses a annotated sentence linearly for probabilty of a transition and a transition '''
        count = sentence.count( '(' )
        if count  == 0:
            print 'Error: Non-valid sentence!'
            return database

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
                    if terms[0] in probability:
                        if terms[1] in probability[terms[0]]:
                            probability[terms[0]][terms[1]] += 1
                        else:
                            probability[terms[0]][terms[1]] = 1
                    else:
                        probability[terms[0]] = {terms[1]: 1}

                    # Update transition database
                    if terms[1] in transition:
                        if terms[0] in transition[terms[1]]:
                            pass
                        else:
                            transition[terms[1]].append( terms[0] )
                    else:
                        transition[terms[1]] = [terms[0]]

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
                    if left_term in probability:
                        if right_term in probability[left_term]:
                            probability[left_term][right_term] += 1
                        else:
                            probability[left_term][right_term] = 1
                    else:
                        probability[left_term] = {right_term: 1}

                    # Update transition database
                    if right_term in transition:
                        if left_term in transition[right_term]:
                            pass
                        else:
                            transition[right_term].append( left_term )
                    else:
                        transition[right_term] = [left_term]

                    del temp_db[depth+1] 
                depth -= 1
                iterator = right_pos
                iterator_status = False
        return probability, transition

class CKY():
    def __init__( self, probability, transition):
        self.probability = probability
        self.transition = transition

    def run( self, sentence ):
        words = sentence.split( ' ' )
        n     = len( words )
        score = dict()
        for i in range(n+1):
            for j in range(n+1):
                score[(i,j)] = dict()

        # Step 1 search terminal possibilities and save them with probability 
        for i in range(n):
            poss_rules = transition[ words[i] ]
            for rule in poss_rules:
                print 'Rule added:', rule, '->', words[i]
                score[(i, i+1)][( rule, words[i])] = \
                    probability[ rule ][ words[i] ] / float( sum( probability[ rule ].values() ) )

        # Step 2 handle unaries
            added = True
            while added:
                added = False
                candidates = score[(i, i+1)].keys()
                # All possible rules for a unary
                for candidate in candidates:
                    if candidate[0] in transition:
                        poss_unaries = transition[ candidate[0] ]
                        for unary in poss_unaries:
                            P = ( probability[ unary ][ candidate[0] ] / float( sum( probability[ rule ].values() ) ) ) * score[(i, i+1)][candidate]
                            if not( (unary, candidate[0]) in score[(i, i+1)] ) or P > score[(i, i+1)][candidate]:
                                print 'Unary Found:', unary, '->', candidate[0]
                                score[(i, i+1)][(unary, candidate[0])] = P
                                added = True
        for key in score:
            print key, score[key]
if __name__ == '__main__':
    x = Parser()
    #probability, transition = x.parse_document( '../data/wsj.02-21.training.nounary' )
    #x.save_database( probability, 'database_p.p' )
    #x.save_database( transition,  'database_t.p' )
    #x.save_database( x.parse_document( '../data/wsj.02-21.training.nounary' ), 'database1.p' )
    probability = x.load_database( 'database_p.p' )
    transition  = x.load_database( 'database_t.p' )
    sentence = '`` The equity market was illiquid .'
    y = CKY( probability, transition )
    y.run( sentence )
