from germalemma import GermaLemma
import re

def gl_lemma(token, pos):

    pattern1 = re.compile("^[NV]")
    pattern2 = re.compile("^(ADJ|ADV)")

    lemmatizer = GermaLemma()

    i = 0
    lemma = []
    for t in token:

        if pattern1.match(pos[i]):
            lemma.append(lemmatizer.find_lemma(t, pos[i][0]))
            continue
        if pattern2.match(pos[i]):
            lemma.append(lemmatizer.find_lemma(t, pos[i][:3]))
            continue

        lemma.append(0)

    return lemma