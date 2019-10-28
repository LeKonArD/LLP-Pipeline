from flair.data import Sentence
from flair.models import SequenceTagger

def flair_ner_base(tokens):

    data = Sentence(" ".join(tokens))
    tagger = SequenceTagger.load('de-ner')
    tagger.predict(data)
    tagged = data.to_dict(tag_type='ner')

    labels = [x["type"] for x in tagged["entities"]]
    print(labels)