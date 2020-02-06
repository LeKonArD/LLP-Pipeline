import subprocess
import os

from llppipeline.base import PipelineModule, ProgressBar

class Marmot(PipelineModule):

    def __init__(self, jarfile='resources/marmot-2015-10-22.jar', modelfile='resources/de.marmot'):
        self.jarfile = jarfile
        self.modelfile = modelfile

    def targets(self):
        return {'morphology-marmot', 'pos-marmot'}

    def prerequisites(self):
        return {'token', 'sentence'}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        sentences = prerequisite_data['sentence']

        if not os.path.exists("temp"):
            os.mkdir("temp")

        with open("temp/marmot_input", 'w') as f:
            sent = sentences[0]
            for tok, s in zip(tokens, sentences):
                if s != sent:
                    f.write('\n')

                f.write(tok + '\n')
                sent = s

        proc = subprocess.Popen("java -cp %s marmot.morph.cmd.Annotator --model-file %s --test-file form-index=0,temp/marmot_input --pred-file /dev/stdout" % (self.jarfile, self.modelfile),
                                    shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

        bar = ProgressBar('Marmot', max=len(prerequisite_data['token']))

        morph = []
        pos = []
        with proc.stdout as f:
            line = f.readline()
            while line:
                if not line.strip():
                    line = f.readline()
                    continue

                fields = line.split('\t')
                if len(fields) >= 6:
                    pos += [fields[5].strip().split("|")[0]]
                else:
                    pos += ['_']

                if len(fields) >= 8:
                    morph += [self._convert_morph(fields[7].strip())]
                else:
                    morph += [{}]

                bar.next()

                line = f.readline()
        bar.finish()

        return {
            'morphology-marmot': morph,
            'pos-marmot': pos
        }

    def _convert_morph(self, morphstr):
        ret = {}

        for s in morphstr.split("|"):
            t = s.split("=")
            if len(t) == 2:
                ret[t[0]] = t[1]

        return ret
