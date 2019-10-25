from somajo import SentenceSplitter


def sent_smo(tokens):

    sentence_splitter = SentenceSplitter()
    sentences = sentence_splitter.split(tokens)

    return sentences
