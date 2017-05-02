from __future__ import unicode_literals
import pytest
import codecs
from jursegtok import corpus

FREQ_PARAGRAPHS = 12
FREQ_TOKENS = 123

class TestCorpus(object):
    """
    tests if corpus methods work 
    """
    def setup(self):
        testdoc = corpus.OJDocument('testdata/test_896152.html')
        paragraphs = testdoc.paragraphs()
        with codecs.open("testdata/test_expected.txt", mode='w', encoding='utf-8') as outfile:
            for para  in paragraphs:
                outfile.write(unicode(para) + "\n")
        
    def test_paragraphs(self):
        """
        checks if number of paragraphs equals assertion.
        """
        assert FREQ_PARAGRAPHS == len(paragraphs)
 
    def test_whitespace_tokenizing(self):
        pass
   
    def test_token_consistency(self):
        """
        tests if tokens 
        """
        pass
            
    


