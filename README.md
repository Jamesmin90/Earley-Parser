# Earley-Parser

Implementation of an Earley parser that reads in a grammar and lexicon, then reads in and parses tokenized input sentences (one sentence per line) from a file. The goal is to output whether the sentence is grammatical or not.
The start symbol of the grammar is the first symbol that appears in the grammar file.

## Require

Python >= 3.9

## How to run

Python earley.py grammar.txt lexicon.txt
