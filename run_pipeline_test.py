import sys
import os
import argparse

# change working directory to script location
cwd = os.curdir
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import llppipeline.util.config as config
from llppipeline.base import Pipeline

import llppipeline.filereader
import llppipeline.tokenizer
import llppipeline.tagger
import llppipeline.corenlp
import llppipeline.spacy
import llppipeline.morphology
import llppipeline.marmot
import llppipeline.parzu

parser = argparse.ArgumentParser()
parser.add_argument('infiles', nargs='+', type=argparse.FileType('r'))
parser.add_argument('--no-progress', dest='progress', action='store_false')
parser.add_argument('--output-dir', dest='outdir', type=str, default=os.path.join(cwd, 'output'))
parser.set_defaults(progress=True)
config.args = parser.parse_args()

pipeline = Pipeline()

reader = llppipeline.filereader.PlainReader(None)
pipeline.register_module(reader)
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

result = {}

if not os.path.exists(config.args.outdir):
    os.mkdir(config.args.outdir)

for f in config.args.infiles:
    print("Processing file " + f.name, file=sys.stderr)
    reader.input_file = f

    del(result)
    result = pipeline.make(set(targets))

    with open(os.path.join(cwd, config.args.outdir, os.path.basename(f.name)), 'w') as outfile:
        print("Writing to " + outfile.name, file=sys.stderr)
        print('\t'.join(targets), file=outfile)
        for i in range(len(result[targets[0]])):
            fields = [str(result[t][i]) for t in targets]
            print('\t'.join(fields), file=outfile)
