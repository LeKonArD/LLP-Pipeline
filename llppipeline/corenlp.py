from llppipeline.base import PipelineModule, ProgressBar
import subprocess
import os
import pexpect
import sys

class CoreNLP(PipelineModule):

    def __init__(self, classpath='resources/stanford-corenlp-full-2018-10-05/*'):
        self.proc = pexpect.spawn('/bin/sh', echo=False, timeout=None, encoding='utf-8')
        self.proc.sendline('stty -icanon')
        self.proc.logfile = sys.stderr
        self.proc.sendline('java '
                           '-cp "%s" '
                           'edu.stanford.nlp.pipeline.StanfordCoreNLP '
                           '-props StanfordCoreNLP-german.properties '
                           '-outputFormat conll '
                           '-tokenize.language whitespace '
                           '-threads 8 '
                           '-annotators tokenize,ssplit,pos,parse,depparse,ner ' % classpath
                           #'-isOneDocument true' % classpath
            )

        self.proc.expect_exact('Entering interactive shell')
        self.proc.readline()
        self.proc.expect_exact('NLP> ')
        self.proc.delaybeforesend = 0
        self.proc.logfile = None

    def targets(self):
        return {'pos-corenlp', 'syntax-corenlp', 'entities-corenlp'}

    def prerequisites(self):
        return {'token', 'sentence'}

    def make(self, prerequisite_data):
        sent = prerequisite_data['sentence']
        tokens = prerequisite_data['token']

        syntax = []
        pos = []
        entities = []
        sentlen = 0

        for i in ProgressBar('CoreNLP', max=len(tokens)).iter(range(len(tokens))):
            tok = tokens[i]

            if i+1 < len(tokens) and sent[i] == sent[i+1]:
                self.proc.send(tok + ' ')
                sentlen = sentlen + 1
            else:
                self.proc.send(tok)
                sentlen = sentlen + 1
                self.proc.sendline()

                i = 0
                while i < sentlen:
                    line = self.proc.readline().strip()
                    fields = list(map(lambda f: f.strip(), line.strip().split('\t')))

                    if len(fields) < 6:
                        continue

                    pos += [fields[3]]
                    headpos = int(fields[5]) - int(fields[0])
                    syntax += [(fields[6], headpos)]
                    entities += [fields[4]]
                    i = i + 1
                sentlen = 0
                self.proc.expect_exact('NLP> ')

        return {'pos-corenlp': pos, 'syntax-corenlp': syntax, 'entities-corenlp': entities}
