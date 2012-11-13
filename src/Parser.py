
class Parser():
    def __init__(self):
        pass

    def parse(self, sentence):
        count = sentence.count( '(' )
        if count  == 0:
            print 'Error: Non-valid sentence!'
            return
        database = dict()
        temp_db  = dict()

        length = len( sentence )
        
        depth = 0
        done = False
        iterator = sentence.find( '(' )
        # If the current parenthesis is open (True) or closed (False)
        iterator_status = True

        while( iterator+1 != length ):
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
                    left_term  = temp_db[depth]
                    left_term  = left_term.pop()
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
        for key in database:
            print key, database[key]

# We zoeken het eerste haakje (
# Dan zoeken we het volgende haakje ( wat een hoger level is )
# Dan sla je er wat er tussen is als de left term.


if __name__ == '__main__':
    string = "(TOP (S (PP (IN In) (NP (NP (DT an) (NP@ (NNP Oct.) (NP@ (CD 19) (NN review)))) (NP@ (PP (IN of) (NP (`` ``) (NP@ (NP (DT The) (NN Misanthrope)) (NP@ ('' '') (PP (IN at) (NP (NP (NNP Chicago) (POS 's)) (NP@ (NNP Goodman) (NNP Theatre)))))))) (PRN (-LRB- -LRB-) (PRN@ (`` ``) (PRN@ (S (NP (VBN Revitalized) (NNS Classics)) (VP (VBP Take) (VP@ (NP (DT the) (NN Stage)) (PP (IN in) (NP (NNP Windy) (NNP City)))))) (PRN@ (, ,) (PRN@ ('' '') (PRN@ (NP (NN Leisure) (NP@ (CC &) (NNS Arts))) (-RRB- -RRB-)))))))))) (S@ (, ,) (S@ (NP (NP (NP (DT the) (NN role)) (PP (IN of) (NP (NNP Celimene)))) (NP@ (, ,) (NP@ (VP (VBN played) (PP (IN by) (NP (NNP Kim) (NNP Cattrall)))) (, ,)))) (S@ (VP (VBD was) (VP (ADVP (RB mistakenly)) (VP@ (VBN attributed) (PP (TO to) (NP (NNP Christina) (NNP Haag)))))) (. .))))) )"
    #string = "(TT (TEST tr)(PP tf))" 
    x = Parser()
    x.parse( string )
