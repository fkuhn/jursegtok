#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

import nltk

import hickle

from jursegtok.corpus import OJDocument
from jursegtok.utils import get_data
from segtok import segmenter, segmenter_test, tokenizer


# COMMON = '/home/kuhn/Dev/github/jursegtok/data/common_abbrv.txt'


class JurSentTokenizer(object):

    def __init__(self):

        self.jur_abbreviations = self.get_abbreviations()

        self.sent_tokenizer = self.get_tokenizer_model()
        self.sent_tokenizer_alt = self.get_tokenizer_model('jursentok1500.hkl')

        # must remove ending abbreviation stops to feed as parameters.
        # inline abbreviation stops are kept

        # self.sent_tokenizer._params.abbrev_types.update(set(self.jur_abbreviations))
        self.sent_tokenizer._params.abbrev_types.update(set(self.jur_abbreviations))

    def get_abbreviations(self, abbreviations='legal_abbrv.txt'):
        """
        Reads and prepares abbreviations from a text file found in data.
        param: abbreviations: file
        return: abbreviations: set
        """
        abbrev_file = codecs.open(get_data('legal_abbrv.txt'), encoding='utf8')
        return set(unicode(abbrev.strip().rstrip('.'))
                   for abbrev in abbrev_file)

    def get_tokenizer_model(self, model='jursentok.hkl'):
        """
        Reads and prepares a pretrained tokenizer model hickle-serialized data.
        param: model: file
        return: tokenizer_object: tokenizer object

        Parameters
        ----------
        model :

        """
        tokenizer_object = hickle.load(get_data(model), safe=False)
        return tokenizer_object

    def sentence_tokenize(self, textdata):
        """
        Takes a document string and returns a list of sentence segments.

        Parameters
        ----------
        textdata : basestring or OJDocument
            the input document

        Returns
        -------
        sentences : list(basestring)
            a list of sentences
        """
        if isinstance(textdata, OJDocument):
            textdata = textdata.plain_text

        sentences = self.check_abbrev(self.sent_tokenizer.tokenize(textdata))
        return sentences

    def check_abbrev(self, sentences):
        """
        checks if abbreviations have been mistakingly been seen as sentence terminal
        :param sentences:
        :return:
        """
        for sentence in sentences:

            tokens = tokenizer.space_tokenizer(sentence)
            if tokens[-2] in self.jur_abbreviations and tokens[-1] == u'.':
                tokens[-2] = tokens[-2] + u'.'
                tokens.remove(tokens[-1])
                # get the next sentence
                nextsenttokens = tokenizer.web_tokenizer(sentences[sentences.index(sentence) + 1])
                tokens.extend(nextsenttokens)
                sentence_update = u' '.join(tokens)
                sentences[sentences.index(sentence)] = sentence_update
                sentences = sentences.remove(sentences[sentences.index(sentence) + 1])
                return sentences
            else:
                return sentences

    def add_abbreviations(self, abbreviations):
        """
        From a given list, add abbreviations to the tokenizer.
        Needs a list of abbreviations.
        :param abbreviations: list
        """
        self.jur_abbreviations.add(unicode(abbreviations))

    def train_tokenizer(self, trainsetpath):
        """
        (Re-)trains the tokenizer from a given OJCorpusPlain iterator.
        params: path to training set: string
        """

        trainset = OJCorpusPlain(trainsetpath)
        trainer = nltk.tokenize.punkt.PunktTrainer()
        trainer.INCLUDE_ALL_COLLOCS = True
        trainer.INCLUDE_ABBREV_COLLOCS = True

        for fname, document in trainset_iterator:
            try:
                trainer.train(document)
            except:
                continue
        trainer.finalize_training()
        self.sent_tokenizer = trainer.get_params()
