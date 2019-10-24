import spacy as sp

def tagpos_sp(tokens):

    nlp = sp.load("de_core_news_sm")
    doc = nlp.tokenizer.tokens_from_list(tokens)
    doc = nlp.tagger(doc)
    postags = [token.pos_ for token in doc]

    return postags
