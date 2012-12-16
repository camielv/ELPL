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
        parse_information = dict()
        parse_information['probability_terminal']     = dict()
        parse_information['probability_non-terminal'] = dict()
        parse_information['transition_terminal']      = dict()
        parse_information['transition_non-terminal']  = dict()

        for sentence in file:
            parse_information = self.parse_sentence(sentence, parse_information)

        return self.renameLowTerminals(parse_information)

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
                    
                    # Check if its a number
                    try:
                        float(terms[1])
                        terms[1] = 'XXXNUMBER'
                    except ValueError:
                    # Make terminal uppercase
                        terms[1] = terms[1].upper()

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
                            parse_information['transition_terminal'][terms[1]][terms[0]] += 1
                        else:
                            parse_information['transition_terminal'][terms[1]][terms[0]] = 1
                    else:
                        parse_information['transition_terminal'][terms[1]] = {terms[0]: 1}

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
                            parse_information['transition_non-terminal'][right_term][left_term] += 1
                        else:
                            parse_information['transition_non-terminal'][right_term][left_term] = 1
                    else:
                        parse_information['transition_non-terminal'][right_term] = {left_term: 1}

                    del temp_db[depth+1] 
                depth -= 1
                iterator = right_pos
                iterator_status = False
        return parse_information

    def renameLowTerminals(self, parse_information):
        name = 'XXXUNKNOWN'
        terminals = parse_information['transition_terminal'].keys()
        parse_information['transition_terminal'][name] = dict()
        for terminal in terminals:
            if sum(parse_information['transition_terminal'][terminal].values()) < 6:
                # Update databases and remove low freq words
                tags = parse_information['transition_terminal'][terminal].keys()
                for tag in tags:
                    if name in parse_information['probability_terminal'][tag]:
                        parse_information['probability_terminal'][tag][name] += 1
                    else:
                        parse_information['probability_terminal'][tag][name] = 1

                    if tag in parse_information['transition_terminal'][name]:
                        parse_information['transition_terminal'][name][tag] += 1
                    else:
                        parse_information['transition_terminal'][name][tag] = 1

                    del parse_information['probability_terminal'][tag][terminal]
                del parse_information['transition_terminal'][terminal]
        return parse_information
