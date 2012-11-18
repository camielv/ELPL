import cPickle as pickle

class Parser():
    def __init__(self):
        pass

    def save_database(self, database, path):
        pickle.dump( database, open( path, 'wb' ) )

    def load_database(self, path):
        return pickle.load( open( path, 'rb' ) )

    def parse_document(self, path):
        file = open( path, 'r+' )
        database = dict()
        i =0
        for sentence in file:
            database = self.parse_sentence( sentence, database )

        return database

    def parse_sentence(self, sentence, database):
        count = sentence.count( '(' )
        if count  == 0:
            print 'Error: Non-valid sentence!'
            return database

        temp_db  = dict()
        length = len( sentence )
        depth = 0
        iterator = sentence.find( '(' )
        # If the current parenthesis is open (True) or closed (False)
        iterator_status = True

        while( depth >= 0 ):
            left_pos  = sentence.find( '(', iterator+1 )
            right_pos = sentence.find( ')', iterator+1 )

            if left_pos < right_pos and left_pos != -1:
                # Case if previous parenthesis is open and current is open.
                if iterator_status:
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
                    temp = sentence[iterator+1:right_pos]
                    terms = temp.split( ' ' )
                    if terms[0] in database:
                        if terms[1] in database[terms[0]]:
                            database[terms[0]][terms[1]] += 1
                        else:
                            database[terms[0]][terms[1]] = 1
                    else:
                        database[terms[0]] = {terms[1]: 1}
                    # Saving for higher depth
                    if depth in temp_db:
                        temp_db[depth].append( terms[0] )
                    else:
                        temp_db[depth] = [ terms[0] ]
                # Case if previous parenthesis is closed and current is closed.
                else:
                    left_term = temp_db[depth][len(temp_db[depth])-1]
                    right_term = tuple(temp_db[depth+1])
                    if left_term in database:
                        if right_term in database[left_term]:
                            database[left_term][right_term] += 1
                        else:
                            database[left_term][right_term] = 1
                    else:
                        database[left_term] = {right_term: 1}
                    del temp_db[depth+1] 
                depth -= 1
                iterator = right_pos
                iterator_status = False
        return database


if __name__ == '__main__':
    x = Parser()
    database = x.load_database( 'database1.p' )
    print database
    #x.save_database( x.parse_document( '../data/wsj.02-21.training.nounary' ), 'database1.p' )
