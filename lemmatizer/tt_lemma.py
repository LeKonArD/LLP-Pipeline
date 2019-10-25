import treetaggerwrapper

def lemma_tt(tokens):

    tagger = treetaggerwrapper.TreeTagger(TAGLANG="de")
    lemma = tagger.tag_text(tokens, tagonly=True)
    lemma = [x.split("\t")[2] for x in postags]

    return lemma