import os
import pytest
import types
import nltk
import codecs
from jursegtok import tokenizer, corpus
from jursegtok.utils import get_data

# setup
tok = tokenizer.JurSentTokenizer()
testdoc = corpus.OJDocument('testdata/test_896152.html')
test_plaintext = testdoc.plain_text()
expected_text = codecs.open('testdata/test_expected.txt', mode='r', encoding='utf-8')

"""
This module contains tests for the jursegtok tokenizer
"""


class TestTokenizer(object):
    """
    initialize the tokenizer,
    sentence tokenize example docs and test the expected outcome.
    """

    def test_simple_tokenizing(self):

        sentence = "Das ist das Haus vom Nikolaus."
        sentence_count = 1

        assert(sentence_count == len(tok.sentence_tokenize(sentence)))

    def test_document_tokenizing(self):

        result_sentences = tok.sentence_tokenize(test_plaintext)

        expected_sentences = expected_text.readlines()

        assert(len(result_sentences) == len(expected_sentences))

