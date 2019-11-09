from llppipeline.base import PipelineModule
from flair.data import Sentence
from flair.models import SequenceTagger

class Spacy(PipelineModule):

    def __init__(self, token_prereq, model='de-pos'):
        self.token_prereq = token_prereq
        self.tagger = SequenceTagger.load(model)

    def targets(self):
        return {'pos-flair', 'entity-flair'}

    def prerequisites(self):
        return {self.token_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data[self.token_prereq]
        data = Sentence(tokens)
        self.tagger.predict(data)

        return {
            'pos-flair': [x.get_tag("pos").value for x in data],
            'entity-flair': [x.get_tag("ner").value for x in data],
        }

