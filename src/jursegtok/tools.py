
__author__ = 'kuhn'

import os
import codecs
import logging
from lxml import etree

import hickle
# from segtok.segmenter import split_single, split_multi
from segtok import segmenter
from sklearn.feature_extraction.text import CountVectorizer


# define constants
HTML_PARSER = etree.HTMLParser()
OJCORPUS_DIR = '/home/kuhn/Data/ojc_joint_set'
tokenizer = CountVectorizer().build_tokenizer()
# jurtokenizer = tokenizer.JurSentTokenizer()
jur_segmenter = hickle.load('/home/kuhn/github/jursegtok/data/jursentok.hkl', safe=False)

HEADERS = [u'Rubrum',u'Tenor', u'Tatbestand', u'Gründe', u'Entscheidungsgründe']


def convert2sentences(corpuspath, outputpath):
    """
    converts raw ojc data to sentence segmented plaintext
    :param corpuspath:
    :param outputpath:
    :return:
    """
    corpus = OJCorpusPlain(corpuspath)
    output = os.path.abspath(outputpath)
    for name, document in corpus:

        with codecs.open(os.path.join(output, name.rstrip('.html')+'_sentences.txt'), encoding='utf-8', mode='w') as sentencetokenized:
            tokenized = sentencelist2string(jur_segmenter.tokenize(document))
            sentencetokenized.write(tokenized)
        sentencetokenized.close()


def sentencelist2string(sentencelist):
    """
    takes a list of sentences and returns a
    concatenated string of all elements.
    """
    for element in sentencelist:
        element.strip('\t\n')
        if element in HEADERS:
            element = element.uppercase()
            element = element + '\n'

    sentences = '\n'.join(sentencelist)

    return sentences

def open_remote_corpus():
    """
    opens the remote corpus resource via ssh
    :return:
    """
    pass

def count_tokens(corpuspath):
    tokens_count = int()
    tok_generator = sklearn_tokjursent_generator(corpuspath)
    for tokenized_sentence in tok_generator:
        tokenlen = len(tokenized_sentence)
        tokens_count += tokenlen
    return tokens_count


def count_sentences(corpusiterator):
    """
    counts all sentences a corpusiterator
    :param corpusiterator: an iterator over the corpus resource
    :return: sentnumber: int
    """
    sent_number = int()
    for filename, sentencegenerator in corpusiterator:
        for sentence in sentencegenerator:
            sent_number += 1
    return sent_number


def jursegment_sent_generator(document):
    """
    a sentence generator that uses the retrained nltk sentence tokenizer
    :param document: list of str
    :return:
    """
    for segment in document:
        for sentence in jur_segmenter.tokenize(segment):
            if sentence.strip():
                yield sentence


def segtok_sent_generator(document):
    """
    returns a generator over the sentences of a document.
    each jursegtok is represented as a string.

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


def sklearn_toksent_generator(corpus_path):
    ojcorpus = OJCorpus(corpus_path)
    for fname, sentences in ojcorpus:
        for sentence in sentences:
            tokenized_sentence = tokenizer(sentence)
            if len(tokenized_sentence) > 1:
                yield tokenized_sentence


def sklearn_tokjursent_generator(corpus_path):
    ojcorpus = OJCorpusJurSentTok(corpus_path)
    for fname, sentences in ojcorpus:
        for sentence in sentences:
            tokenized_sentence = tokenizer(sentence)
            if len(tokenized_sentence) > 1:
                yield tokenized_sentence


class OJCorpusPOSIterator(object):
    """
    Iterator that takes a corpuspath and returns a filename and an
    ordered list of token-POS tuples of an document.
    """
    def __init__(self, corpus_path):
        self.corpus_path = os.path.abspath(corpus_path)
        self.file_names = iter(os.listdir(self.corpus_path))

    def __iter__(self):
        return self

    def next(self):
        file_name = self.file_names.next()




class OJCorpusPlain(object):
    """
    returns a plain textstring of a file
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
            logging.error('Assertion Error. No root: ' + file_name)
            return
        return file_name, ' '.join(tree.xpath('//article//text()'))


class OJCorpusJurSentTok(object):
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
            return
        return file_name, jursegment_sent_generator(tree.xpath('//article//text()'))


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
            return
        return file_name, segtok_sent_generator(tree.xpath('//article//text()'))
