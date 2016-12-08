#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import gzip
import glob
import logging
import os
import random
import shutil
import hickle
import numpy
import operator
from jursegtok import corpus

from lxml import etree
from sklearn.feature_extraction.text import CountVectorizer
from nltk import tokenize
from jursegtok.tokenizer import JurSentTokenizer
from jursegtok.utils import get_data, find_files
from segtok import tokenizer as segtoktokenizer
from segtok import segmenter


# define constants
HTML_PARSER = etree.HTMLParser()
COUNT_TOKENIZER = CountVectorizer().build_tokenizer()
JUR_SEGMENTER = hickle.load(get_data('jursentok.hkl'), safe=False)


# HEADERS = [u'Rubrum',u'Tenor', u'Tatbestand', u'Gründe', u'Entscheidungsgründe']
HEADERS = [u'## Tenor', u'## Tatbestand', u'## Grunde',
           u'## Gründe', u'## Entscheidungsgründe', u'Entscheidungs']


def token_period_freqlist(corp, periods='.', wordnr=1000, minbifrq=1,
                         mintrifrq=1, ranksize=100 ):
    """
    Uses a simple whitespace tokenizer, looks for all
    tokens that end with a period and returns a
    dictionary of them and all counts.
    :param corpuspath:
    :param wordnr:
    :param minbifrq:
    :param mintrifrq:
    :param ranksize:
    :return:
    """
    tokenperiods = dict()
    for doc in corp:
        tokenlist = doc.whitespace_tokenized()
        for token in tokenlist:
            if token[-1] in periods and not tokenperiods.get(token):
                tokenperiods.update({token: 1})
            elif token[-1] in periods and tokenperiods.get(token):
                tpcount = tokenperiods.get(token)
                tokenperiods.update({token: tpcount+1})
    tokenperiods_sorted = sorted(tokenperiods.items(),
                                 key=operator.itemgetter(1))
    return tokenperiods_sorted


def find_tokenpunct(doc):
    """
    whitespace tokenizes a document
    and returns a frequency dict of all

    :param doc:
    :return:
    """


def punctpref_freq(corpus, output, k=100):
    """
    frequency list of all (Token,'.') tuples.
    :param corpus: OJCorpus: OJCorpus object
    :param output: str: filename of output file
    :param k: int: range of frequency list
    :return:
    """
    ws_tkn = tokenize.WhitespaceTokenizer()
    freqs = numpy.array()
    for doc in corpus:
        pass






def random_sampling(corpuspath, outputpath='/tmp', k=10, debug=False):
    """
    randomly selects k elements from a corpus and
    copies them to an output path
    :param corpuspath:
    :param number:
    :return:
    """
    files = list(find_files(corpuspath, '*.html.gz'))
    samples = random.sample(files, k)
    for filepath in samples:
        shutil.copy(filepath, outputpath)
        if debug:
            print(os.path.basename(filepath))


def random_sentenced_docs(corpuspath, outputpath='/tmp',
                          k=10, debug=False, gz=True):
    """
    random sampling with already sentence segmented
    documents.
    :param corpuspath:
    :param outputpath:
    :param k: int - number of samples
    :param debug:
    :param gz: True when .html.gz reference
    :return:
    """

    if gz:
        files = list(find_files(corpuspath, '*.html.gz'))
    else:
        files = list(find_files(corpuspath, '*.html'))

    samples = random.sample(files, k)

    for filepath in samples:

        fname = os.path.basename(filepath).split('.')[0]+'.txt'

        doc = corpus.OJDocument(filepath)
        sentences = doc.sentences()
        with codecs.open(os.path.join(outputpath, fname), mode='w', encoding='utf8') as sent:
            for sentence in sentences:
                sentence = " ".join(sentence.split())
                sent.write(sentence+'\n')



def build_hickle_word_sequences(corpuspath, output):
    """
    inefficient list based word sequence building
    dumps a hickle object as file
    :param corpuspath:
    :param output: path and name of the outputfile
    :return:
    """
    corp = corpus.OJCorpus(corpuspath, gz=False)
    tkn = tokenize.WordPunctTokenizer()
    outputf = codecs.open(output, encoding='utf8', mode='w')
    for doc in corp:
        # FIXME hickles cannot be used for multiple objects
        # to one hickle file at the moment
        # use h5py and its create_dataset function directly
        # must encode to unicode to pass on to hickle
        words = [word.encode('utf8') for word in (tkn.tokenize(doc.plain_text()))]

        hickle.dump(words, outputf, mode='a')


def convert2sentences(corpuspath, outputpath):
    """
    converts raw ojc data to sentence segmented plaintext files
    :param corpuspath:
    :param outputpath:
    :return:
    """
    corpus = corpus.OJCorpus(corpuspath)
    output = os.path.abspath(outputpath)
    jst = JurSentTokenizer()
    for name, document in corpus:
        outfilepath = os.path.join(output, name.rstrip('.html') + '_sentences.txt')
        with codecs.open(outfilepath, encoding='utf-8', mode='w') as sentencetokenized:
            tokenized = sentencelist2string(jst.sentence_tokenize(document))
            sentencetokenized.write(tokenized)


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
        for sentence in JUR_SEGMENTER.tokenize(segment):
            if sentence.strip():
                yield sentence


def sklearn_toksent_generator(corpus_path):
    ojcorpus = corpus.OJCorpus(corpus_path)
    for fname, sentences in ojcorpus:
        for sentence in sentences:
            tokenized_sentence = COUNT_TOKENIZER(sentence)
            if len(tokenized_sentence) > 1:
                yield tokenized_sentence


def sklearn_tokjursent_generator(corpus_path):
    ojcorpus = OJorpusJurSentTok(corpus_path)
    for fname, sentences in ojcorpus:
        for sentence in sentences:
            tokenized_sentence = COUNT_TOKENIZER(sentence)
            if len(tokenized_sentence) > 1:
                yield tokenized_sentence

