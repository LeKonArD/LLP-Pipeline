from llppipeline.base import PipelineModule, ProgressBar
from germalemma import GermaLemma
import sys
import re

class GermaLemma(PipelineModule):

    def __init__(self, pos_prereq):
        self.pos_prereq = pos_prereq
        self.lemmatizer = GermaLemma(tiger_corpus = 'resources/tiger_release_aug07.corrected.16012013.conll09')

    def targets(self):
        return {'lemma-germalemma'}

    def prerequisites(self):
        return {'token', self.pos_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        pos = prerequisite_data[self.pos_prereq]

        pattern1 = re.compile("^[NV]")
        pattern2 = re.compile("^(ADJ|ADV)")

        lemmas = []
        for (token, postag) in ProgressBar('GermaLemma', max=len(prerequisite_data['token'])).iter(zip(tokens, pos)):
            try:
                if pattern1.match(postag):
                    lemmas += [self.lemmatizer.find_lemma(token, postag)]
                elif pattern2.match(postag):
                    lemmas += [self.lemmatizer.find_lemma(token, postag[:3])]
                else:
                    lemmas += ['_']
            except Exception as e:
                sys.stderr.write(f"Lemmatizing {token} ({postag}) raised exception: {e}\n")
                lemmas += ['_']

        return {
            'lemma-germalemma': lemmas
        }
