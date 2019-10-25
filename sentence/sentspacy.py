import spacy as sp

def sent_sp(tokens):

    nlp = sp.load("de_core_news_sm")
    doc = nlp.tokenizer.tokens_from_list(tokens)
    doc = nlp.tagger(doc)
    doc = nlp.parser(doc)

    sent = 0
    sentences = []
    for token in doc:

        if token.is_sent_start:

            sent += 1

        sentences.append(sent)
    print(sentences)
    return sentences