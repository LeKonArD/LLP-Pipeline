from llppipeline.base import PipelineModule
from flair.data import Sentence
from flair.models import SequenceTagger

class Spacy(PipelineModule):

    def __init__(self, model='de-pos'):
        self.tagger = SequenceTagger.load(model)

    def targets(self):
        return {'pos-flair', 'entity-flair'}

    def prerequisites(self):
        return {'token'}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        data = Sentence(tokens)
        self.tagger.predict(data)

        return {
            'pos-flair': [x.get_tag("pos").value for x in data],
            'entity-flair': [x.get_tag("ner").value for x in data],
        }

