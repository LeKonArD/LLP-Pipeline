from flair.data import Sentence
from flair.models import SequenceTagger

def flair_pos_base(tokens):

    data = Sentence(" ".join(tokens))
    tagger = SequenceTagger.load('de-pos')
    tagger.predict(data)
    pos = [x.get_tag("pos").value for x in data]
   
    return pos

def flair_pos_fine(tokens):

    data = Sentence(" ".join(tokens))
    tagger = SequenceTagger.load('de-pos-fine-grained')
    tagger.predict(data)
    pos = [x.get_tag("pos").value for x in data]
   
    return pos