__author__ = 'kuhn'

import nltk
import codecs


class JurSentTokenize(object):

    def _init__(self):

        self.abbreviations = codecs.open('../../data/legal_abbrv.txt', encoding='utf-8').readlines()

        self.sent_tokenize = nltk.data.load('tokenizers/punkt/german.pickle')
        self.sent_tokenize._params.abbrev_types.update(set(self.abbreviations))

    def sentence_tokenize(self, data):

        sent = self.sent_tokenize.tokenize(data)

        return sent


