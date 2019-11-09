from llppipeline.base import PipelineModule
import re
import subprocess
import demorphy

class Zmorge(PipelineModule):

    def __init__(self, token_prereq, transducer='resources/fst-infl2', modelfile='resources/zmorge-20150315-smor_newlemma.ca'):
        self.token_prereq = token_prereq
        self.transducer = transducer
        self.modelfile = modelfile

    def targets(self):
        raise {'morphology-zmorge'}

    def prerequisites(self):
        raise {self.token_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data[self.token_prereq]
        input_str = tokens.join("\n")

        process = subprocess.run([self.transducer, self.modelfile], text=True, capture_output=True)
        lines = process.stdout.split("\n")
        pat = re.compile("^> ")
        negative = re.compile("^no result for")

        infls = []
        morph_output = []
        while True:
            try:
                while not pat.match(next(lines)):
                    infl = next(lines)
                    if not negative.match(infl):
                        infls += [infl]

                morph_output += [infls]
                infls = []
            except StopIteration:
                break


        return {'morphology-zmorge': morph_output}

class DEMorphy(PipelineModule):

    def __init__(self, token_prereq):
        self.token_prereq = token_prereq

    def targets(self):
        raise {'morphology-demorphy'}

    def prerequisites(self):
        raise {self.token_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data[self.token_prereq]
        analyzer = demorphy.Analyzer(char_subs_allowed=True)

        morph_output = list(map(lambda tok: list(analyzer.analyze(tok)), tokens))

        return {'morphology-demorphy': morph_output}

