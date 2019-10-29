import subprocess
import os
import re

def get_hyphens(zmorge_out):

    hyphens = re.sub("<[^>]+>", " ", zmorge_out)
    hyphens = re.sub("^\s+|\s+$", "", hyphens)
    hyphens = re.sub("\s", "-", hyphens)

    return hyphens

def get_genus(zmorge_out, male, fem, neu):

    if male.match(zmorge_out):
        return "m"

    if fem.match(zmorge_out):
        return "f"

    if neu.match(zmorge_out):
        return "n"

    return "O"

def get_numerus(zmorge_out, pl, sg):

    if pl.match(zmorge_out):
        return "pl"

    if sg.match(zmorge_out):
        return "sg"

    return "O"

def morph_zmorge(tokens, path_to_model):

    male = re.compile(".*<Masc>")
    fem = re.compile(".*<Fem>")
    neu = re.compile(".*<Neut>")

    pl = re.compile(".*<Pl>")
    sg = re.compile(".*<Sg>")

    for token in tokens:
        out = os.popen('echo \"'+token+'\" |fst-infl2 '+path_to_model).read()
        print(out)
        out = out.split("\n")[1]

        gen = get_genus(out, male, fem, neu)
        hyphens = get_hyphens(out)
        num = get_numerus(out, pl, sg)

        print(hyphens)
        print(gen)
        print(num)

        print(out)




morph_zmorge(["verliebt"], "/home/konle/LLP-Pipeline/models/zmorge-20150315-smor_newlemma.ca")
