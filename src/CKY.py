'''
    Implementation of CKY based on Stanford slides.
'''
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
            if words[i] in self.parse_information['transition_terminal']:
                # Find all possible rules to terminal and save them
                poss_rules = self.parse_information['transition_terminal'][ words[i] ]
                for rule in poss_rules:
                    key = (rule,)
#                    print 'New Rule Found:', rule, '->', words[i]
                    score[(i, i+1)][ key ] = \
                        self.parse_information['probability_terminal'][ rule ][ words[i] ] / \
                        float( sum( self.parse_information['probability_terminal'][ rule ].values() ) )
                    trace[(i, i+1)][ key ] = words[i]

        # Step 2 handle unaries
                added = True
                while added:
                    added = False
                    # Look for possible candidates for unary and find their
                    # corresponding transition
                    candidates = score[(i, i+1)].keys()
                    for candidate in candidates:
                        if candidate in self.parse_information['transition_non-terminal']:
                            poss_unaries = self.parse_information['transition_non-terminal'][ candidate ]
                            for unary in poss_unaries:
                                P = ( self.parse_information['probability_non-terminal'][ unary ][ candidate ] / \
                                    float( sum( self.parse_information['probability_non-terminal'][ unary ].values() ) ) ) * \
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
                print "Terminal", words[i], "does not exist"
                print words
                print i
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
                            if consequence in self.parse_information['transition_non-terminal']:
                                poss_rules = self.parse_information['transition_non-terminal'][consequence]
                                for poss_rule in poss_rules:
                                    P = score[(begin, split)][candidate_A] * \
                                        score[(split, end)][candidate_B] * \
                                        self.parse_information['probability_non-terminal'][poss_rule][consequence] / \
                                        float(sum(self.parse_information['probability_non-terminal'][ poss_rule ].values() ) )
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
                        if candidate in self.parse_information['transition_non-terminal']:
                            poss_unaries = self.parse_information['transition_non-terminal'][ candidate ]
                            for unary in poss_unaries:
                                P = ( self.parse_information['probability_non-terminal'][ unary ][ candidate ] / \
                                    float( sum( self.parse_information['probability_non-terminal'][ unary ].values() ) ) ) * \
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
        if(abs(i-j) == 1):
            if isinstance(tag, str):
                return tag
            else:
                rule = self.trace[(i,j)][tag]
                return tag[0], self.viterbi(i, j, rule)
        rule = self.trace[(i,j)][tag]
        if len(rule) == 1:
            return tag[0], self.viterbi(i, j, rule)
        else:
            x = self.viterbi(i, rule[1], (rule[0][0],))
            y = self.viterbi(rule[1], j, (rule[0][1],))
            # Handling NP@ case
            if tag[0].count('@') > 0:
                return x, y
            # Handling %%%%% case
            elif tag[0].count('%') > 0 and tag[0].count('%') % 5 == 0:
                pos_tags = tuple(tag[0].split('%%%%%'))
                count_tags = len(pos_tags)
                branch = (pos_tags[count_tags-1], x, y)
                for i in range(len(pos_tags)-2,0-1,-1):
                    branch = (pos_tags[i], test)
                return branch
            # Handling tuples
            if isinstance(x[0], tuple) and isinstance(y[0], tuple):
                return tag[0], x[0], x[1], y[0], y[1]
            elif isinstance(x[0], tuple):
                return tag[0], x[0], x[1], y
            elif isinstance(y[0], tuple):
                return tag[0], x, y[0], y[1]
                    
            return tag[0], x, y
