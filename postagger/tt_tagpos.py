import treetaggerwrapper


def tagpos_tt(tokens):

    tagger = treetaggerwrapper.TreeTagger(TAGLANG="de")
    postags = tagger.tag_text(tokens, tagonly=True)
    postags = [x.split("\t")[1] for x in postags]

    return postags
