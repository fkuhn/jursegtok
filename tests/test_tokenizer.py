import os
import pytest
import types
import nltk
from jursegtok import tokenizer, corpus

TESTDOC = corpus.OJDocument('testdata/896152.html')


"""
This module contains tests for the jursegtok tokenizer
"""

TESTFILE = 'testdata/896152.html'


class TestTokenizer(object):
    """
    initialize the tokenizer,
    sentence tokenize example docs and test the expected outcome.
    """
	@staticmethod
    def setup(self):

        testdoc = corpus.OJDocument(TESTFILE)
        plain = testdoc.plain_text()
        assert type(plain, types.StringType)
        assert len(plain) > 0

        tok = tokenizer.JurSentTokenizer()
        assert type(tok.get_tokenizer_model(), nltk.tokenize.punkt.PunktSentenceTokenizer)

	@staticmethod
    def test_abbreviations(self):
        pass
    @staticmethod
    def test_tokenizing(self):
        pass
