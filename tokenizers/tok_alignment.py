
def align_token_structure(tokens):
    chap_struc = []
    chapter_num = 0
    para_struc = []
    para_num = 0

    if isinstance(tokens[0][0], list):

        for chapter in tokens:
            chap_struc = chap_struc+len([x for y in chapter for x in y])*[chapter_num]
            chapter_num+=1
            for paragraph in chapter:
                para_struc = para_struc+len(paragraph)*[para_num]
                para_num+=1

        return chap_struc, para_struc, [z for q in [x for y in tokens for x in y] for z in q]

    else:

        for chapter in tokens:
            chap_struc = chap_struc + len(chapter) * [chapter_num]

        return chap_struc, [x for y in tokens for x in y]
