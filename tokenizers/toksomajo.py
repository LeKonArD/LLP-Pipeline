from somajo import Tokenizer

def token_smo(structure):

    tokenizer = Tokenizer(split_camel_case=True, token_classes=False, extra_info=False)

    if isinstance(structure[0], list):
        tokenlist = []

        for chapter in structure:

            tokenlist.append([tokenizer.tokenize_paragraph(x) for x in chapter])

    else:

        tokenlist = [tokenizer.tokenize_paragraph(x) for x in structure]

    return tokenlist