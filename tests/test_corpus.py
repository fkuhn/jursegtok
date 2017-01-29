from __future__ import unicode_literals
import pytest
import codecs
from jursegtok import corpus
# first a simple "test"

testdoc = corpus.OJDocument('896152.html')


paragraphs = testdoc.paragraphs()

print len(paragraphs)

with codecs.open("testurteil.txt", mode='w', encoding='utf-8') as outfile:
    for para  in paragraphs:
        outfile.write(unicode(para) + "\n")



