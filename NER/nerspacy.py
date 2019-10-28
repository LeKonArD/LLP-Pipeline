import spacy as sp


def sp_ner(tokens):

    nlp = sp.load("de_core_news_sm")
    doc = nlp.tokenizer.tokens_from_list(tokens)
    doc = nlp.entity(doc)
    ner_labels = []
    ner_pos = []
    for ent in doc.ents:
        ner_labels.append(ent.label_)
        ner_pos.append(ent.start)

    ner = []
    i = 0
    for ind in list(range(0, len(tokens), 1)):

        if ind in ner_pos:
            ner.append(ner_labels[i])
            i += 1
        else:
            ner.append(0)

    return ner
