import sys
import os
import codecs
from jursegtok import cli, tokenizer, corpus


indata = sys.argv[1]
outdata = sys.argv[2]
js = tokenizer.JurSentTokenizer()

def main():

    if os.path.isfile(indata):
        with corpus.OJDocument(indata) as textdata:
            output = js.sentence_tokenize(textdata)

        with codecs.open(outdata, mode='w', encoding='utf-8') as outfile:

            for sentence in output:
                outfile.writeline(sentence)

if __name__ == "__main__":
    main()
