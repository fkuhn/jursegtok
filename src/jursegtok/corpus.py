#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import gzip
import logging
import nltk
import json

from lxml import etree
from segtok import tokenizer as segtoktokenizer

from jursegtok.utils import find_files
from jursegtok.tokenizer import JurSentTokenizer

HTML_PARSER = etree.HTMLParser()


class CorpusIndexer(object):
    """
    Indexing of a Corpus with elasticsearch.
    See notebook for details.
    """
    pass


class OJCorpus(object):
    """
    This class represents a corpus of gzipped openjur.de court decision
    HTML files as an Iterable over ``OJDocument`` instances.
    """
    def __init__(self, corpus_path, gz=True):
        self.gz = gz
        self.corpus_path = os.path.abspath(corpus_path)

        if self.gz:
            self.file_paths = find_files(corpus_path, '*.html.gz')
        else:
            self.file_paths = find_files(corpus_path, '*.html')

    def regenerate_paths(self):
        """
        ``self.file_paths`` is a generator. If you have iterated over all
        the files once, you'll need to call this method to iterate over them
        again.
        """
        if self.gz:
            self.file_paths = find_files(self.corpus_path, '*.html.gz')
        else:
            self.file_paths = find_files(self.corpus_path, '*.html')

    def __iter__(self):
        return self

    def next(self):
        return OJDocument(self.file_paths.next())


class OJDocument(object):
    """
    This class represents a document from the openjur.de corpus of court
    decisions in various formats.
    """
    def __init__(self, document_path):
        self.document_path = document_path
        tree = self._get_html_tree()

        info_tree = tree.xpath("//div[contains(@id, 'info')]")[0]

        self.file_name = os.path.basename(self.document_path)
        self.court = info_tree.xpath("//ul/li/p/a")[0].text
        # self.date = info_tree.xpath("//ul/li/p")[0].text
        self.date = info_tree.xpath("//ul/li/p")[1].text
        self.file_id = info_tree.xpath("//ul/li/p")[2].text  # aktenzeichen
        self.verdict_type = info_tree.xpath("//ul/li/p")[3].text  # typ
        self.source = info_tree.xpath("//ul/li/p")[4].text  # fundstelle
        self.process = info_tree.xpath("//ul/li/p")[5].text
        field_of_law_root = info_tree.xpath("//span[contains(@class, 'rechtsgebiete')]/a")
        self.field_of_law = u', '.join([fol.text for fol in field_of_law_root])

    def meta2json(self):
        """
        Returns a json string containing the meta information
        of the document.
        :return:
        """
        metadict = dict()
        metadict = {'filename': self.file_name,
                    'date': self.date,
                    'court': self.court,
                    'file_id': self.file_id,
                    'decision_type': self.verdict_type,
                    'decision_source': self.source,
                    'process': self.process,
                    'fields_of_law': self.field_of_law,
                    'document_path': self.document_path}
        return json.dumps(metadict)

    def _get_html_tree(self):
        """returns an LXML etree representation of the input HTML file"""
        tree = None
        try:
            tree = etree.parse(self.document_path, parser=HTML_PARSER)
        except AssertionError:
            logging.error('Assertion Error. No Root: ' + self.document_path)
        return tree

    # @property
    def filename(self):
        return os.path.basename(self.document_path)

    # @property
    def raw_html(self):
        with gzip.open(self.document_path, 'r') as html_file:
            return html_file.read()

    # @property
    def plain_text(self):
        tree = self._get_html_tree()
        return u' '.join(tree.xpath('//article//text()'))

    # @property
    def sentences(self):
        """
        returns a list of sentences. Sentence segmentation is done using a
        retrained nltk sentence tokenizer.
        """
        # tree = self._get_html_tree()
        # apply the sentence tokenizer
        jsent_tokenizer = JurSentTokenizer()
        return jsent_tokenizer.sentence_tokenize(self.plain_text())
        # return jursegment_sent_generator(tree.xpath('//article//text()'))

    # @property
    def tokens(self):
        """
        Returns a list of tokens created by running the plain text of the
        document through ``segtok``'s ``word_tokenizer``.

        NOTE: This tokenizer does not consider sentence boundaries at all.
        """
        return segtoktokenizer.word_tokenizer(self.plain_text)

    def whitespace_tokenized(self):
        """
        returns a whitespace tokenized token list of the document.
        :return:
        """
        wstkn = nltk.tokenize.WhitespaceTokenizer()
        return wstkn.tokenize(self.plain_text())


def train_tokenizer(self, trainsetpath, setsize=1000):
    """
    (Re-)trains the tokenizer from a given OJCorpusPlain iterator.
     Parameters
    ----------
    trainsetpath : string - path to the training set
    setsize : int - the number of docs used for training
    """

    trainset = OJCorpus(trainsetpath)
    trainer = nltk.tokenize.punkt.PunktTrainer()
    trainer.INCLUDE_ALL_COLLOCS = True
    trainer.INCLUDE_ABBREV_COLLOCS = True
    epoch = 0
    for fname, document in trainset:
        if setsize == epoch:
            break
        try:
            trainer.train(document)
            epoch += 1
        except :
            continue
    trainer.finalize_training()
    self.sent_tokenizer = trainer.get_params()

class TrainCorpus(object):
    """
    This class represents a corpus of gzipped openjur.de court decision
    HTML files as an Iterable over ``OJDocument`` instances.
    """
    def __init__(self, corpus_path, gz=True):
        self.gz = gz
        self.corpus_path = os.path.abspath(corpus_path)

        if self.gz:
            self.file_paths = find_files(corpus_path, '*.html.gz')
        else:
            self.file_paths = find_files(corpus_path, '*.html')

    def regenerate_paths(self):
        """
        ``self.file_paths`` is a generator. If you have iterated over all
        the files once, you'll need to call this method to iterate over them
        again.
        """
        if self.gz:
            self.file_paths = find_files(self.corpus_path, '*.html.gz')
        else:
            self.file_paths = find_files(self.corpus_path, '*.html')

    def __iter__(self):
        return self

    def next(self):
        return OJDocument(self.file_paths.next())