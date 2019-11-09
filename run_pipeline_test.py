from llppipeline.base import Pipeline

import llppipeline.filereader
import llppipeline.tokenizer
import llppipeline.tagger
import llppipeline.corenlp
import llppipeline.spacy

input_file = 'test_file.txt'
pipeline = Pipeline()

pipeline.register_module(llppipeline.filereader.PlainReader(input_file))
pipeline.register_module(llppipeline.tokenizer.Syntok())
pipeline.register_module(llppipeline.tagger.RNNTagger(token_prereq='token-syntok', sent_prereq='sentence-syntok'))
pipeline.register_module(llppipeline.corenlp.CoreNLP(token_prereq='token-syntok'))
pipeline.register_module(llppipeline.spacy.Spacy(token_prereq='token-syntok'))

targets = {'token-syntok', 'sentence-syntok',
           'pos-rnntagger', 'morphology-rnntagger'}
           'pos-corenlp', 'syntax-corenlp', 'sentence-corenlp',
           'pos-spacy', 'syntax-spacy'}

result = pipeline.make(targets)

for i in range(len(result['token-syntok'])):
    print(result['token-syntok'][i], result['sentence-syntok'][i],
          result['pos-rnntagger'][i], result['morphology-rnntagger'][i])
          result['sentence-corenlp'][i], result['pos-corenlp'][i], result['syntax-corenlp'][i],
          result['pos-spacy'][i], result['syntax-spacy'][i])





