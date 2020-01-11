from llppipeline.base import Pipeline

import llppipeline.filereader
import llppipeline.tokenizer
import llppipeline.tagger
import llppipeline.corenlp
import llppipeline.spacy
import llppipeline.morphology
import llppipeline.marmot

input_file = 'test_file.txt'
pipeline = Pipeline()

pipeline.register_module(llppipeline.filereader.PlainReader(input_file))
pipeline.register_module(llppipeline.tokenizer.Syntok())
pipeline.register_module(llppipeline.corenlp.CoreNLP(token_prereq='token-syntok'))
pipeline.register_module(llppipeline.spacy.Spacy(token_prereq='token-syntok'))
pipeline.register_module(llppipeline.tagger.TreeTagger(token_prereq='token-syntok'))
pipeline.register_module(llppipeline.tagger.RNNTagger(token_prereq='token-syntok', sent_prereq='sentence-syntok'))
pipeline.register_module(llppipeline.tagger.SoMeWeTa(token_prereq='token-syntok', sent_prereq='sentence-syntok'))
pipeline.register_module(llppipeline.tagger.Clevertagger(sent_prereq='sentence-syntok',token_prereq='token-syntok',smor_prereq='morphology-zmorge'))
pipeline.register_module(llppipeline.marmot.Marmot(token_prereq='token-syntok', sent_prereq='sentence-syntok'))
pipeline.register_module(llppipeline.morphology.Zmorge(token_prereq='token-syntok'))
pipeline.register_module(llppipeline.morphology.DEMorphy(token_prereq='token-syntok'))

targets = ['token-syntok', 'sentence-syntok',
           'lemma-spacy', 'pos-spacy', 'syntax-spacy', 'entity-spacy',
           'pos-corenlp', 'syntax-corenlp', 'entities-corenlp', 'sentence-corenlp',
           'lemma-treetagger', 'pos-treetagger',
           'pos-rnntagger', 'morphology-rnntagger', 'lemma-rnntagger',
           'pos-someweta',
           'pos-clevertagger',
           'morphology-marmot', 'pos-marmot',
           'morphology-zmorge',
           'morphology-demorphy',
           ]

result = pipeline.make(set(targets))

print('\t'.join(targets))
for i in range(len(result[targets[0]])):
    fields = [str(result[t][i]) for t in targets]
    print('\t'.join(fields))
