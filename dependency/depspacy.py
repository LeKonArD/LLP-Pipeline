import spacy as sp


def spdep(tokens):

    nlp = sp.load("de_core_news_sm")
    doc = nlp.tokenizer.tokens_from_list(tokens)
    doc = nlp.parser(doc)
    dep = [token.dep_ for token in doc]
    head = [token.head.i for token in doc]
    
    return dep, head
