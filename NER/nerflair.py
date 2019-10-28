from flair.data import Sentence
from flair.models import SequenceTagger

def flair_ner_base(tokens):

    data = Sentence(" ".join(tokens))
    tagger = SequenceTagger.load('de-ner')
    tagger.predict(data)
    ner = [x.get_tag("ner").value for x in data]
   
    return ner
 