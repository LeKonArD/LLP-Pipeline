from someweta import ASPTagger

def smwt_pos(tokens, sents, model):


    asptagger = ASPTagger()
    asptagger.load(model)

    pos = []
    state = sents[0]
    i = 0
    sent_token = []
    for t in tokens:

        if sents[i] != state:
            possent = asptagger.tag_sentence(sent_token)
            pos.append(possent)
            sent_token = []
            state = sents[i]

        sent_token.append(t)
        i += 1

    possent = asptagger.tag_sentence(sent_token)
    pos.append(possent)
    pos = [x for y in pos for x in y]

    return pos
