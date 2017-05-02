from __future__ import print_function, unicode_literals
import os
import codecs
import argparse
import tokenizer

PARSER = argparse.ArgumentParser()
# PARSER.add_argument("--dir", const='' )
PARSER.add_argument("intext")


def main():
    """
    main method processing the cli arguments
    :return:
    """
    arguments = PARSER.parse_args()
    text = arguments.intext
    tk = tokenizer.JurSentTokenizer()

    if os.path.isfile(text):
        out = process_file(text, tk)
    elif isinstance(text, basestring):
        out = tk.sentence_tokenize(text)

    return out


def process_file(tfile, tk):
    with codecs.open(tfile, encoding='utf-8') as tf:
        content = tf.read()
        out = tk.sentence_tokenize(content)

    return out

