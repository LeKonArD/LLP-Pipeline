import spacy as sp

def nounchunk_sp(tokens):

    nlp = sp.load("de_core_news_sm")
    doc = nlp.tokenizer.tokens_from_list(tokens)
    doc = nlp.tagger(doc)


    chunk_end = []
    chunk_start = []
    chunkroot = []

    for chunk in nlp.parser(doc).noun_chunks:

        chunkroot.append(chunk.root.i)
        chunk_start.append(chunk.start)
        chunk_end.append(chunk.end)

    chunkind = 1
    NC = []
    NC_root = []
    state = False

    for ind in list(range(0, len(doc), 1)):

        if ind in chunkroot:
            NC_root.append("root")
        else:
            NC_root.append(0)

        if ind in chunk_start:
            state = True

        if ind in chunk_end:
            chunkind += 1
            state = False

        if state == True:
            NC.append(chunkind)
        else:
            NC.append(0)

    return NC, NC_root

