__author__ = 'kuhn'

import nltk
import codecs
import os

from segtok import tokenizer
from segtok import segmenter
from segtok import segmenter_test

JUR = '/home/kuhn/PycharmProjects/jursegtok/data/legal_abbrv.txt'
COMMON = '/home/kuhn/PycharmProjects/jursegtok/data/common_abbrv.txt'


class JurSentTokenizer(object):

    def __init__(self):

        self.jur_abbreviations = codecs.open(os.path.abspath(JUR), encoding='utf-8').readlines()

        self.common_abbreviations = codecs.open(os.path.abspath(COMMON), encoding='utf-8').readlines()

        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')

        # must remove ending abbreviation stops to feed as parameters.
        # inline abbreviation stops are kept
        self.jur_abbreviations = [unicode(abbrev.rstrip('\n')) for abbrev in self.jur_abbreviations]
        self.common_abbreviations = [unicode(abbrev.rstrip('\n')) for abbrev in self.common_abbreviations]
        self.jur_abbreviations = [unicode(abbrev.rstrip('.')) for abbrev in self.jur_abbreviations]
        self.common_abbreviations = [unicode(abbrev.rstrip('.')) for abbrev in self.common_abbreviations]

        # self.sent_tokenizer._params.abbrev_types.update(set(self.jur_abbreviations))
        self.sent_tokenizer._params.abbrev_types.update(set(self.common_abbreviations))

    def sentence_tokenize(self, data):

        sentences = self.check_abbrev(self.sent_tokenizer.tokenize(data))
        return sentences

    def check_abbrev(self, sentences):
        """
        checks if abbreviations have been mistakingly been seen as sentence terminal
        :param sentences:
        :return:
        """

        for sentence in sentences:

                tokens = tokenizer.web_tokenizer(sentence)
                if tokens[-2] in self.common_abbreviations and tokens[-1] == u'.':
                    tokens[-2] = tokens[-2]+u'.'
                    tokens.remove(tokens[-1])
                    # get the next sentence
                    nextsenttokens = tokenizer.web_tokenizer(sentences[sentences.index(sentence)+1])
                    tokens.extend(nextsenttokens)
                    sentence_update = u' '.join(tokens)
                    sentences[sentences.index(sentence)] = sentence_update
                    sentences = sentences.remove(sentences[sentences.index(sentence)+1])
                    return sentences