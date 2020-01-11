from llppipeline.base import PipelineModule
import re
import subprocess
import demorphy

class Zmorge(PipelineModule):

    def __init__(self, transducer='resources/fst-infl2', modelfile='resources/zmorge-20150315-smor_newlemma.ca'):
        self.transducer = transducer
        self.modelfile = modelfile

    def targets(self):
        return {'lemma-zmorge', 'morphology-zmorge'}

    def prerequisites(self):
        return {'token'}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        input_str = '\n'.join(tokens) + '\n'

        process = subprocess.run([self.transducer, self.modelfile], input=input_str, text=True, capture_output=True)
        lines = process.stdout.split("\n")
        pat = re.compile("^> ")
        negative = re.compile("^no result for")

        infls = []
        morph_output = []
        it = iter(lines)
        while True:
            try:
                infl = next(it)
                while not pat.match(infl):
                    if not negative.match(infl):
                        infls += [infl]
                    infl = next(it)

                morph_output += [infls]
                infls = []
            except StopIteration:
                morph_output += [infls]
                break


        return {'morphology-zmorge': morph_output[1:]}

class DEMorphy(PipelineModule):

    def targets(self):
        return {'morphology-demorphy'}

    def prerequisites(self):
        return {'token'}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        analyzer = demorphy.Analyzer(char_subs_allowed=True)

        morph_output = list(map(lambda tok: list(analyzer.analyze(tok)), tokens))

        return {'morphology-demorphy': morph_output}

