from llppipeline.base import PipelineModule
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

        def lemmatize_token(t, postag):
            try:
                if pattern1.match(postag):
                    return self.lemmatizer.find_lemma(t, postag)
                elif pattern2.match(postag):
                    return self.lemmatizer.find_lemma(t, postag[:3])
                else:
                    return 0
            except Exception as e:
                sys.stderr.write(f"Lemmatizing {t} ({postag}) raised exception: {e}\n")
                return 0

        return {
            'lemma-germalemma': list(map(lambda x: lemmatize_token(x[0], x[1]), zip(tokens, pos)))
        }
