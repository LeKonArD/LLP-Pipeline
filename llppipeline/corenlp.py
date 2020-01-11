from llppipeline.base import PipelineModule
import subprocess
import os

class CoreNLP(PipelineModule):

    def __init__(self, classpath='resources/stanford-corenlp-full-2018-10-05/*'):
        self.classpath = classpath

    def targets(self):
        return {'pos-corenlp', 'syntax-corenlp', 'entities-corenlp', 'sentence-corenlp'}

    def prerequisites(self):
        return {'token'}

    def make(self, prerequisite_data):
        if not os.path.exists("temp"):
            os.mkdir("temp")

        with open("temp/corenlp_input", 'w') as f:
            for tok in prerequisite_data['token']:
                f.write(tok + '\n')

        subprocess.run("java -cp \"%s\" -mx8g edu.stanford.nlp.pipeline.StanfordCoreNLP "
                                 "-props StanfordCoreNLP-german.properties -outputFormat conll "
                                 "-tokenize.language whitespace -annotators tokenize,ssplit,pos,parse,depparse,ner "
                                 "-file temp/corenlp_input -outputDirectory temp"
                                 % self.classpath, shell=True, stdout=subprocess.PIPE)

        syntax = []
        pos = []
        entities = []
        sent = []
        sentid = 0
        with open("temp/corenlp_input.conll") as f:
            for line in f:
                if not line.strip():
                    sentid = sentid + 1
                    continue

                fields = list(map(lambda f: f.strip(), line.split('\t')))
                pos += [fields[3]]
                headpos = int(fields[5]) - int(fields[0])
                syntax += [(fields[6], headpos)]
                entities += [fields[4]]
                sent += [sentid]

        return {'pos-corenlp': pos, 'syntax-corenlp': syntax, 'entities-corenlp': entities, 'sentence-corenlp': sent}
