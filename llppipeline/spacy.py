from llppipeline.base import PipelineModule
import spacy
from spacy.tokens import Doc

class Spacy(PipelineModule):

    def targets(self):
        return {'lemma-spacy', 'pos-spacy', 'syntax-spacy', 'entity-spacy'}

    def prerequisites(self):
        return {'token'}

    def make(self, prerequisite_data):
        nlp = spacy.load("de_core_news_sm")

        nlp.tokenizer = lambda x: Doc(nlp.vocab, words=prerequisite_data['token'])
        doc = nlp('')

        ner_out = len(doc) * ["_"];
        for ent in doc.ents:
            ent_len = ent.end - ent.start
            ner_out[ent.start:ent.end] = ent_len * [ent.label_]

        return {
            'pos-spacy': [token.tag_ for token in doc],
            'lemma-spacy': [token.lemma_ for token in doc],
            'syntax-spacy': [(token.dep_, token.head.i - token.i) for token in doc],
            'entity-spacy': ner_out
        }

