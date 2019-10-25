import spacy as sp


def token_sp(structure):

    nlp = sp.load("de_core_news_sm")

    if isinstance(structure[0], list):
        tokenlist = []

        for chapter in structure:

            tokenlist.append([[token.text for token in nlp(x) if token.text != "\n"] for x in chapter])

    else:

        tokenlist = [[token.text for token in nlp(x) if token.text != "\n"] for x in structure]

    return tokenlist
