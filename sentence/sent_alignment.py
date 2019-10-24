
def align_token_sentence(sentences):

    sent_count = 0
    sent_struc = []
    for sentence in sentences:
        sent_struc = sent_struc + len(sentence)*[sent_count]
        sent_count+=1

    return sent_struc