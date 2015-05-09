__author__ = 'kuhn'

import nltk
import codecs


class JurSentTokenizer(object):

    def _init__(self):

        self.jur_abbreviations = codecs.open('../../data/legal_abbrv.txt', encoding='utf-8').readlines()

        self.common_abbreviations = codecs.open('../../data/common_abbrv.txt', encoding='utf-8').readlines()

        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')

        # must remove ending abbreviation stops to feed as parameters.
        # inline abbreviation stops are kept
        for abbrev in self.jur_abbreviations:
            abbrev.rstrip('.')

        for abbrev in self.common_abbreviations:
            abbrev.rstrip('.')

        self.sent_tokenizer._params.abbrev_types.update(set(self.jur_abbreviations))
        self.sent_tokenizer._params.abbrev_types.update(set(self.common_abbreviations))

    def sentence_tokenize(self, data):

        return self.sent_tokenizer.tokenize(data)


