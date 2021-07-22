#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from collections import defaultdict
from typing import DefaultDict, Dict, Tuple


class Parser:
    def __init__(self, grammarfile, lexiconfile):
        self.grammar = self.read_grammar(grammarfile)
        self.lexicon = self.read_lexicon(lexiconfile)

    # Read in grammar
    # grammar["XY"] returns all rules with "XY" as first element
    @staticmethod
    def read_grammar(filename: str) -> DefaultDict[str, list]:
        grammar = defaultdict(list)
        with open(filename) as file:
            for line in file:
                fields = line.split()
                lhs = fields[0]
                rhs = tuple(fields[1:])
                grammar[lhs].append(rhs)
        return grammar

    # Read in lexicon
    # lexicon["word"] returns all possible tags of the word "word"
    @staticmethod
    def read_lexicon(filename: str) -> Dict[str, Tuple[str]]:
        lexicon = {}
        with open(filename) as file:
            for line in file:
                fields = line.split()
                word = fields[0]
                tags = tuple(fields[1:])
                lexicon[word] = tags
        return lexicon

    def predict(self, nonterm: str, pos: int):
        # Enter all rules whose right-hand side begins with nonterm
        for rhs in self.grammar[nonterm]:
            self.add(nonterm, rhs, 0, pos, pos)

    def scan(self, token: str):
        # The word is not in the dictionary
        if token not in self.lexicon:
            print('unknown word:', token, file=sys.stderr)
        else:
            # Create new chart entry for word
            self.chart.append({*()})
            for tag in self.lexicon[token]:
                # Enter all possible word types from the dictionary into chart
                self.add(tag, (token,), 1, len(self.chart) - 2, len(self.chart) - 1)

    def complete(self, nonterm: str, startpos: int, endpos: int):
        # Go through all point rules ending at startpos
        for (lhs, rhs, dotpos, startpos, endpos2) in self.chart[startpos]:
            # Test whether the point rule can be completed with the point rule passed as argument
            if len(rhs) > dotpos and rhs[dotpos] == nonterm:
                self.add(lhs, rhs, dotpos + 1, startpos, endpos)

    def add(self, lhs: str, rhs: tuple, dotpos: int, startpos: int, endpos: int):
        self.chart[endpos].add((lhs, rhs, dotpos, startpos, endpos))
        # Constituent completely recognised
        if len(rhs) == dotpos:
            if (lhs, startpos, endpos) not in self.compl_args:
                if lhs in self.grammar:
                    self.compl_args.add((lhs, startpos, endpos))
                self.complete(lhs, startpos, endpos)
        # Constituent not completely recognized
        elif rhs[dotpos] in self.grammar and (rhs[dotpos], endpos) not in self.pred_args:
            self.pred_args.add((rhs[dotpos], endpos))
            self.predict(rhs[dotpos], endpos)

    def parse(self, tokens: list) -> bool:
        # Initialise data structures
        self.tokens = tokens
        self.pred_args = {*()}
        self.compl_args = {*()}
        self.chart = [{*()}]
        start = "S"
        self.chart[0].add(("S'", (start,), 0, 0, 0))
        self.pred_args.add((start, 0))
        # Call pred operation for start-symbol
        self.predict(start, 0)
        # Call scan operation for each token
        for token in self.tokens:
            self.scan(token)

        # Does the point rule have all the desired properties?
        if ("S'", (start,), 1, 0, len(self.tokens)) in self.chart[-1]:
            return True

        return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: parser.py grammar lexicon textfile")

    parser = Parser(sys.argv[1], sys.argv[2])

    # Read input sentences
    with open(sys.argv[3]) as file:
        for line in file:
            tokens = line.split()
            if len(tokens) > 0:
                print(line)
                print(parser.parse(tokens))
                print()
                print("------------------")
                print()
