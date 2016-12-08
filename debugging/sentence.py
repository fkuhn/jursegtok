from jursegtok import tokenizer, corpus

doc = corpus.OJDocument('../tests/896152.html')
tkn = tokenizer.JurSentTokenizer()

output = tkn.sentence_tokenize(doc.plain_text())

print output