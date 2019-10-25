import treetaggerwrapper

def token_tt(structure):

    tokenizer = treetaggerwrapper.TreeTagger(TAGLANG='de')

    if isinstance(structure[0], list):
        tokenlist = []

        for chapter in structure:

            tokenlist.append([tokenizer.tag_text(x, prepronly=True) for x in chapter])

    else:

        tokenlist = [tokenizer.tag_text(x, prepronly=True) for x in structure]

    return tokenlist