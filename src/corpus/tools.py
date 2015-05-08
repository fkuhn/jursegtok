__author__ = 'kuhn'

import os
import codecs
import nltk
import logging
from lxml import etree
from segtok.segmenter import split_single, split_multi
from segtok import segmenter
from sklearn.feature_extraction.text import CountVectorizer


def segtok_sent_generator(document):
    """
    returns a generator over the sentences of a document.
    each sentence is represented as a string.

    Parameters
    ----------
    document : list of str
        a plain text document represented as a list of its segments
        (extracted from their corresponding HTML elements)
    """
    for segment in document:
        for sentence in segmenter.split_multi(segment):
            if sentence.strip():
                yield sentence


class OJCorpus(object):
    """
    This class represents a corpus of openjur.de court decision HTML files
    as an Iterable over parsed documents.
    Each parsed document is represented by a (filename, list of sentences) tuple.
    """
    def __init__(self, corpus_path):
        self.corpus_path = os.path.abspath(corpus_path)
        self.file_names = iter(os.listdir(self.corpus_path))

    def __iter__(self):
        return self

    def next(self):
        file_name = self.file_names.next()

        try:
            tree = etree.parse(os.path.join(self.corpus_path, file_name), parser=HTML_PARSER)
        except AssertionError:
            logging.error('Assertion Error. No Root: ' + file_name)
        return file_name, segtok_sent_generator(tree.xpath('//article//text()'))