import sys
import os
import codecs
from jursegtok import cli, tokenizer, corpus


try:
    indata = sys.argv[1]
    outdata = sys.argv[2]

except IndexError as e:
    print "one or more missing parameters"


js = tokenizer.JurSentTokenizer()


def main():
    """
    processes the command line arguments and 
    produces an output
    :return: 
    """
    if os.path.isfile(indata):
        textdata = corpus.OJDocument(indata)
        output = js.sentence_tokenize(textdata.plain_text())
        for item in output:
            print item
            print
            print "***********************************************"
            print
        with codecs.open(outdata, mode='w', encoding='utf-8') as outfile:

            for sentence in output:
                outfile.write(sentence+'\n')

if __name__ == "__main__":
    main()



