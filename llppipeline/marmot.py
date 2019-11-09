import subprocess
import os

from llppipeline.base import PipelineModule

class Marmot(PipelineModule):

    def __init__(self, token_prereq, sent_prereq, jarfile='resources/marmot-2019-10-28.jar', modelfile='resources/de.marmot'):
        self.token_prereq = token_prereq
        self.sent_prereq = sent_prereq
        self.jarfile = jarfile
        self.modelfile = modelfile

    def targets(self):
        return {'morphology-marmot', 'pos-marmot'}

    def prerequisites(self):
        return {self.token_prereq, self.sent_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data[self.token_prereq]
        sentences = prerequisite_data[self.sent_prereq]

        if not os.path.exists("temp"):
            os.mkdir("temp")

        with open("temp/marmot_input", 'w') as f:
            sent = sentences[0]
            for tok, s in zip(tokens, sentences):
                if s != sent:
                    f.write('\n')

                f.write(tok + '\n')
                sent = s

        process = subprocess.run("java -cp %s marmot.morph.cmd.Annotator --model-file %s --test-file form-index=0,temp/marmot_input --pred-file temp/marmout_output"
                                    % (self.jarfile, self.modelfile),
                                    shell=True, capture_output=True)

        morph = []
        pos = []
        with open("temp/marmot_output") as f:
            line = f.readline()
            while line:
                if not line.strip():
                    line = f.readline()
                    continue

                fields = line.split('\t')
                if len(fields) >= 6:
                    pos += [fields[5].strip()]
                else:
                    pos += ['_']

                if len(fields) >= 8:
                    morph += [fields[7].strip()]
                else:
                    morph += ['_']

                line = f.readline()

        return {
            'morphology-marmot': morph,
            'pos-marmot': pos
        }
