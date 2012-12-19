Elements of Language Processing and Learning

Authors:
Anna Keune          (6056547) 
Camiel Verschoor    (6229298)

18 December 2012
-----------------------------
Results can be found here:
    https://github.com/camielv/ELPL/tree/master/results

These source files are an implementation of a tree Parser, CKY and Viterbi algorithm.

Files:
    main.py
    Parser.py
    CKY.py
    
main.py    contains the main function calling the treeparser and the cky+viterbi algorithm
Parser.py  contains the tree parser which saves the extracted rules in dicts of dicts
CKY.py     contains the a 'run' function which runs the CKY algorithm which calls the viterbi function and returns the most likely parse

To run the code:
    $ main.py -c <path_to_training_corpus> -s <path_to_test_sentences> -t <path_to_test_trees>

To display all the options:
    $ main.py --help

As optional arguments it's also possible to set the location of the output file and the sentence length to be processed.

Required arguments:
  -c CORPUS_PATH, --corpus-path CORPUS_PATH
                        Path of the training corpus file.
  -s SENTENCES_PATH, --sentences-path SENTENCES_PATH
                        Path of the test sentences.
  -t TEST_TREES_PATH, --test-trees-path TEST_TREES_PATH
                        Path of the test trees (golden standard file).
                        
Optional arguments:
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        Path of the output file (defaults to 'output.txt').
  -m MAX_SENTENCE_LENGTH, --max-sentence-length MAX_SENTENCE_LENGTH
                        Max length of the sentences (defaults to 15).
