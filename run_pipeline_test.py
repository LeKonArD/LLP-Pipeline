import sys
import os

# change working directory to script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from llppipeline.base import Pipeline

import llppipeline.filereader
import llppipeline.tokenizer
import llppipeline.tagger
import llppipeline.corenlp
import llppipeline.spacy
import llppipeline.morphology
import llppipeline.marmot
import llppipeline.parzu

pipeline = Pipeline()

pipeline.register_module(llppipeline.filereader.PlainReader(sys.stdin))
pipeline.register_module(llppipeline.tokenizer.Syntok())
pipeline.register_module(llppipeline.corenlp.CoreNLP())
pipeline.register_module(llppipeline.spacy.Spacy())
pipeline.register_module(llppipeline.tagger.TreeTagger())
pipeline.register_module(llppipeline.tagger.RNNTagger())
pipeline.register_module(llppipeline.tagger.SoMeWeTa())
pipeline.register_module(llppipeline.tagger.Clevertagger(smor_prereq='morphology-zmorge'))
pipeline.register_module(llppipeline.marmot.Marmot())
pipeline.register_module(llppipeline.morphology.Zmorge())
pipeline.register_module(llppipeline.morphology.DEMorphy())
pipeline.register_module(llppipeline.parzu.Parzu(pos_prereq='pos-clevertagger', smor_prereq='morphology-zmorge'))

targets = ['token-syntok', 'sentence-syntok',
           'lemma-spacy', 'pos-spacy', 'syntax-spacy', 'entity-spacy',
           'pos-corenlp', 'syntax-corenlp', 'entities-corenlp',
           'lemma-treetagger', 'pos-treetagger',
           'pos-rnntagger', 'morphology-rnntagger', 'lemma-rnntagger',
           'pos-someweta',
           'pos-clevertagger',
           'syntax-parzu',
           'morphology-marmot', 'pos-marmot',
           'morphology-zmorge',
           'morphology-demorphy',
           ]

result = pipeline.make(set(targets))

print('\t'.join(targets))
for i in range(len(result[targets[0]])):
    fields = [str(result[t][i]) for t in targets]
    print('\t'.join(fields))
