'''
    Implementation of CKY based on Stanford slides.
'''
class CKY():
    def __init__( self, parse_information):
        self.parse_information = parse_information
        self.score = dict()
        self.trace = dict()

    def run( self, words ):
        n = len( words )

        # Save unknown words
        self.sentence = words[:]
        self.sentence.reverse()

        # Create tables
        score = dict()
        trace = dict()
        for i in range(n+1):
            for j in range(n+1):
                score[(i,j)] = dict()
                trace[(i,j)] = dict()

        # Step 1 search terminal possibilities and save them with their probability
        for i in range(n):
            # Check if number
            try:
                float(words[i])
                words[i] = 'XXXNUMBER'
            except ValueError:
                words[i] = words[i].upper()
                # Check if word exists otherwise cast it to uknown
                if not(words[i] in self.parse_information['transition_terminal']):
                    words[i] = 'XXXUNKNOWN'

            # Find all possible rules to terminal and save them
            poss_rules = self.parse_information['transition_terminal'][words[i]].keys()
            for rule in poss_rules:

                key = (rule,)
                total_count_rule = self.parse_information['probability_terminal'][rule].values()

                # Add non-terminal count of the rule
                if rule in self.parse_information['probability_non-terminal']:
                    total_count_rule += self.parse_information['probability_non-terminal'][rule].values()

                # Update score and trace table
                score[(i, i+1)][key] = self.parse_information['probability_terminal'][rule][words[i]] / \
                                            float(sum(total_count_rule))
                trace[(i, i+1)][key] = words[i]

        # Step 2 handle unaries
            added = True
            while added:
                added = False

                # Look for possible candidates for unary rules and find their corresponding transition
                candidates = score[(i, i+1)].keys()
                for candidate in candidates:

                    if candidate in self.parse_information['transition_non-terminal']:

                        poss_unaries = self.parse_information['transition_non-terminal'][candidate].keys()
                        for unary in poss_unaries:

                            key = (unary,)
                            total_count_rule = self.parse_information['probability_non-terminal'][unary].values()

                            if unary in self.parse_information['probability_terminal']:
                                total_count_rule = self.parse_information['probability_terminal'][unary].values()
            
                            P = ( self.parse_information['probability_non-terminal'][unary][candidate] / \
                                  float(sum(total_count_rule)) ) * score[(i, i+1)][candidate]

                            # When the corresponding transition does not exist or has a higher probability save it
                            if not(key in score[(i, i+1)]):
                                score[(i, i+1)][key] = P
                                trace[(i, i+1)][key] = candidate
                                added = True
                            elif P > score[(i, i+1)][key]:
                                score[(i, i+1)][key] = P
                                trace[(i, i+1)][key] = candidate
                                added = True

        # Step 3 binaries
        # Loop diagonally over the table
        for span in range(2, n+1):
            for begin in range((n - span)+1):

                end = begin + span
                for split in range(begin+1, end):
                    # Possible candidate rules
                    candidates_A = score[(begin, split)].keys()
                    candidates_B = score[(split, end)].keys()
                    for candidate_A in candidates_A:
                        for candidate_B in candidates_B:

                            consequence = (candidate_A[0], candidate_B[0])
                            if consequence in self.parse_information['transition_non-terminal']:

                                poss_rules = self.parse_information['transition_non-terminal'][consequence].keys()
                                for poss_rule in poss_rules:

                                    key = (poss_rule,)
                                    total_count_rule = self.parse_information['probability_non-terminal'][poss_rule].values()

                                    if poss_rule in self.parse_information['probability_terminal']:
                                        total_count_rule = self.parse_information['probability_terminal'][poss_rule].values()
            
                                    P = score[(begin, split)][candidate_A] * \
                                        score[(split, end)][candidate_B] * \
                                        self.parse_information['probability_non-terminal'][poss_rule][consequence] / \
                                        float(sum(total_count_rule))

                                    if not(key in score[(begin, end)]):
                                        score[(begin, end)][key] = P
                                        trace[(begin, end)][key] = (consequence, split)
                                    elif P > score[(begin, end)][key]:
                                        score[(begin, end)][key] = P
                                        trace[(begin, end)][key] = (consequence, split)
        # Step 4 unaries
                added = True
                while added:
                    added = False
                    candidates = score[(begin, end)].keys()

                    # All possible rules for a unary
                    for candidate in candidates:
                        if candidate in self.parse_information['transition_non-terminal']:

                            poss_unaries = self.parse_information['transition_non-terminal'][candidate].keys()
                            for unary in poss_unaries:

                                key = (unary,)
                                total_count_rule = self.parse_information['probability_non-terminal'][unary].values()

                                if unary in self.parse_information['probability_terminal']:
                                        total_count_rule = self.parse_information['probability_terminal'][unary].values()

                                P = ( self.parse_information['probability_non-terminal'][unary][candidate] / \
                                    float( sum( total_count_rule ) ) ) \
                                    * score[(begin, end)][candidate]

                                if not(key in score[(begin, end)]):
                                    score[(begin, end)][key] = P
                                    trace[(begin, end)][key] = candidate
                                    added = True
                                elif P > score[(begin, end)][key]:
                                    score[(begin, end)][key] = P
                                    trace[(begin, end)][key] = candidate
                                    added = True
        self.score = score
        self.trace = trace
        tree = self.viterbi(0, n, ('TOP',))

        return tree[:len(tree)-1] + " )\n"

    def viterbi(self, i, j, tag):
        if(abs(i-j) == 1):
            if isinstance(tag, str):
                return self.sentence.pop()
            else:
                rule = self.trace[(i,j)][tag]
                return "(" + tag[0] + " " + self.viterbi(i, j, rule) + ")"
        rule = self.trace[(i,j)][tag]
        if len(rule) == 1:
            return "(" + tag[0] + " " + self.viterbi(i, j, rule) + ")"
        else:
            x = self.viterbi(i, rule[1], (rule[0][0],))
            y = self.viterbi(rule[1], j, (rule[0][1],))
            # Handling NP@ case
            if tag[0].count('@') > 0:
                return x + " " + y
            # Handling %%%%% case
            elif tag[0].count('%') > 0 and tag[0].count('%') % 5 == 0:
                pos_tags = tuple(tag[0].split('%%%%%'))
                count_tags = len(pos_tags)
                branch = "(" + pos_tags[count_tags-1] + " " +  x + " " +  y + ")"
                for i in range(len(pos_tags)-2,0-1,-1):
                    branch = "(" + pos_tags[i] + " " + branch + ")"
                return branch
            # Handling tuples
            if isinstance(x[0], tuple) and isinstance(y[0], tuple):
                return tag[0], x[0], x[1], y[0], y[1]
            elif isinstance(x[0], tuple):
                return tag[0], x[0], x[1], y
            elif isinstance(y[0], tuple):
                return tag[0], x, y[0], y[1]
                    
            return "(" + tag[0] + " " +  x + " " + y + ")"
