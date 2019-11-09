from llppipeline.base import PipelineModule

from someweta import ASPTagger
import treetaggerwrapper
import os
import subprocess
import sys
import re

class TreeTagger(PipelineModule):

    def __init__(self, token_prereq):
        self.tt = treetaggerwrapper.TreeTagger(TAGLANG="de")
        self.token_prereq = token_prereq

    def targets(self):
        return {'lemma-treetagger', 'pos-treetagger'}

    def prerequisites(self):
        return {self.token_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data[self.token_prereq]
        tagged = self.tt.tag_text(tokens, tagonly=True)
        return {
            'lemma-treetagger': [x.split("\t")[2] for x in tagged],
            'pos-treetagger': [x.split("\t")[1] for x in tagged]
        }

class SoMeWeTa(PipelineModule):

    def __init__(self, token_prereq, sent_prereq, model='resources/german_newspaper_2018-12-21.model'):
        self.asptagger = ASPTagger()
        self.asptagger.load(model)
        self.token_prereq = token_prereq
        self.sent_prereq = sent_prereq

    def targets(self):
        return {'pos-someweta'}

    def prerequisites(self):
        return {self.token_prereq, self.sent_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data[self.token_prereq]
        sentences = prerequisite_data[self.sent_prereq]

        sent_end = 0
        input = []

        while sent_end < len(sentences):
            sent_start = sent_end
            sent_end = sent_start
            while sent_end < len(sentences) and sentences[sent_start] == sentences[sent_end]:
                sent_end += 1

            input += [tokens[sent_start:sent_end]]

        tagged_sentences = self.asptagger.tag(input)
        return {
            'pos-someweta': [t for sent in tagged_sentences for t in sent]
        }

class RNNTagger(PipelineModule):

    def __init__(self, token_prereq, sent_prereq):
        self.token_prereq = token_prereq
        self.sent_prereq = sent_prereq

    def targets(self):
        return {'pos-rnntagger', 'morphology-rnntagger', 'lemma-rnntagger'}

    def prerequisites(self):
        return {self.token_prereq, self.sent_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data[self.token_prereq]
        sentences = prerequisite_data[self.sent_prereq]

        if not os.path.exists("temp"):
            os.mkdir("temp")

        with open("temp/rnntagger_input", 'w') as f:
            sent = sentences[0]
            for tok, s in zip(tokens, sentences):
                if s != sent:
                    f.write('\n')

                f.write(tok + '\n')
                sent = s
            f.write('\n')

        process = subprocess.run("sh ./resources/rnn-tagger-german.sh temp/rnntagger_input %s" % sys.executable,
                       shell=True, text=True, stdout=subprocess.PIPE)

        lines = process.stdout.split("\n")
        pos = []
        morph = []
        lemma = []
        for line in lines:
            if line == "":
                continue

            fields = line.split("\t")
            split = re.split("\\.", fields[1], maxsplit=1)

            if re.match('^\\$.*', fields[1]):
                pos += [fields[1]]
                morph += "_"
            else:
                pos += [split[0]]
                if len(split) > 1:
                    morph += [split[1]]
                else:
                    morph += ["_"]
            lemma += [fields[2]]

        return {'pos-rnntagger': pos, 'morphology-rnntagger': morph, 'lemma-rnntagger': lemma}
