#!/usr/bin/env python
from __future__ import unicode_literals
import codecs

import nltk
# import hickle
import pickle
import corpus

from jursegtok.utils import get_data
from segtok import segmenter, segmenter_test, tokenizer

# COMMON = '/home/kuhn/Dev/github/jursegtok/data/common_abbrv.txt'

# jursentmodel = open(get_data('jursentok.hkl'))
jursentmodel = pickle.load(get_data('jursentok.pickle'))
class Abbreviations(object):

    def __init__(self, filepath):
        """
        parses a text file with abbreviations.
        Follows the schema
        abbreviation > paraphrase
        Parameters
        ----------
        filepath
        """
        self.filepath = filepath
        self.abbreviation_dic = {}
        self.abbreviations_list = []
        with codecs.open(self.filepath, mode='r', encoding='utf-8') as abbreviations:
            for line in abbreviations.readlines():
                parts = str.split(str(line), '>')
                self.abbreviation_dic.update({parts[0]: parts[1]})
                # self.atuples.append(tuple(i.rstrip(' ').lstrip(' ') for i in str.split (line,'>')))
            # for item in self.atuples:
            #    self.abbreviations_list.append(item[0])

        self._filepath = filepath
        self.tuples = list()
        self.abbreviations_list =list
        with codecs.open(self._filepath, mode='r', encoding='utf-8') as abbreviations:
            for line in abbreviations.readlines():
                self.tuples.append(tuple(i.rstrip(' ').lstrip(' ') for i in str.split(line,'>')))
            for item in self.tuples:
                self.abbreviations_list.append(item[0])


class JurSentTokenizer(object):

    def __init__(self, tkn='jursentok'):

        if tkn == 'standard':
            self.sent_tokenizer = nltk.tokenize.PunktSentenceTokenizer()
        elif tkn == 'jursentok':
            self.sent_tokenizer = self._get_tokenizer_model()

        self.jur_abbreviations = self.get_abbreviations()

        self.sent_tokenizer._params.abbrev_types.update(set(self.jur_abbreviations))

    @staticmethod
    def get_abbreviations(abbreviations=get_data("legal_abbrv.txt")):
        """
        Reads and prepares abbreviations from a text file found in data.
        param: abbreviations: file
        return: abbreviations: set
        """
        abbrev_file = codecs.open(get_data(abbreviations), encoding='utf8')
        return set(unicode(abbrev.strip().rstrip('.'))
                   for abbrev in abbrev_file)

    @staticmethod
    def _get_tokenizer_model(model=jursentmodel):
        """
        Reads and prepares a pretrained tokenizer model hickle-serialized data.
        param: model: file
        return: tokenizer_object: tokenizer object

        Parameters
        ----------
        model :

        """
        tokenizer_object = hickle.load(model, safe=False)
        return tokenizer_object

    def sentence_tokenize(self, textdata):
        """
        Takes a document string and returns a list of sentence segments.

        Parameters
        ----------
        textdata : basestring of
            the input document

        Returns
        -------
        sentences : list(basestring)
            a list of sentences
        """
        sentences = self.check_abbrev(self.sent_tokenizer.tokenize(textdata))
        # sentences = self.sent_tokenizer.tokenize(textdata)
        return sentences

    def check_abbrev(self, sentences):
        """
        checks if abbreviations have been mistakingly been seen as sentence terminal
        :param sentences:
        :return:
        """
        for sentence in sentences:
            # TODO: Still not working correctly. Abbreviations are not escaped.
            # rewrite method. indexing is wrong
            # simple tokenizing of the sentence.
            ws_tk = nltk.tokenize.WhitespaceTokenizer()
            tokens = ws_tk.tokenize(sentence)

            # try if index is valid
            if len(tokens) <= 3:
                continue
            if tokens[-2] in self.jur_abbreviations and tokens[-1] == '.':
                tokens[-2] = tokens[-2] + u'.'
                tokens.remove(tokens[-1])
                # get the next sentence
                nextsenttokens = tokenizer.web_tokenizer(sentences[sentences.index(sentence) + 1])
                tokens.extend(nextsenttokens)
                sentence_update = u' '.join(tokens)
                sentences[sentences.index(sentence)] = sentence_update
                sentences = sentences.remove(sentences[sentences.index(sentence) + 1])

        return sentences

    def add_abbreviations(self, abbreviations):
        """
        From a given list, add abbreviations to the tokenizer.
        Needs a list of abbreviations.
        :param abbreviations: list
        """
        self.jur_abbreviations.add(unicode(abbreviations))

# todo: rework this method
    def train_tokenizer(self, trainsetpath, setsize=1000):
        """
        (Re-)trains the tokenizer from a given OJCorpusPlain iterator.
        Parameters
        ----------
        trainsetpath : string - path to the training set
        setsize : int - the number of docs used for training
        """
        trainset = corpus.TrainCorpus(trainsetpath)
        trainer = nltk.tokenize.punkt.PunktTrainer()
        trainer.INCLUDE_ALL_COLLOCS = True
        trainer.INCLUDE_ABBREV_COLLOCS = True
        iteration = 0
        for fname, document in trainset:
            if setsize == iteration:
                break
            try:
                trainer.train(document)
                iteration += 1
            except:
                continue
        trainer.finalize_training()
        self.sent_tokenizer = trainer.get_params()


