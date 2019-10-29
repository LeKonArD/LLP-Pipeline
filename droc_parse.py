from structure.rulebased import split_paragraphs, split_chapters, split_paragraphs_in_chapter
from tokenizers.toksomajo import token_smo
from tokenizers.tok_alignment import align_token_structure
from sentence.sentsomajo import sent_smo
from sentence.sent_alignment import align_token_sentence
from postagger.spacy_tagpos import tagpos_sp
from postagger.flair_pos import flair_pos_base, flair_pos_fine
from tokenizers.toktreetagger import token_tt
from tokenizers.tokspacy import token_sp
from postagger.tt_tagpos import tagpos_tt
from sentence.sentspacy import sent_sp
from chunker.sp_nounchunks import nounchunk_sp
from lemmatizer.tt_lemma import lemma_tt
#from lemmatizer.germalemma import gl_lemma
from postagger.someweta_pos import smwt_pos
from NER.nerspacy import sp_ner
from NER.nerflair import flair_ner_base, flair_ner_fine
from morphology.morph_marmot import morph_marmot
from dependency.depspacy import spdep
import pandas as pd
import os

files = os.listdir("/home/konle/DROC/DROC-Release/tsv")

for filename in files:

    tokens = list(pd.read_csv("/home/konle/DROC/DROC-Release/tsv/" + filename, sep="\t", index_col=0)["token"])

    # sent
    sentences_spacy = sent_sp(tokens)

    # pos
    pos_treetagger = tagpos_tt(tokens)

    # dependency
    spdep, sphead = spdep(tokens)

    # NER
    spacy_ner = sp_ner(tokens)
    flair_ner_basic = flair_ner_base(tokens)
    flair_ner_large = flair_ner_fine(tokens)

    # morph
    case_marmot, number_marmot, gender_marmot, person_marmot, tense_marmot, mood_marmot, degree_marmot = morph_marmot(
        tokens, sentences_spacy)

    # chunks
    noun_chunks, noun_chunks_root = nounchunk_sp(tokens)

    table = pd.DataFrame()
    table["sentence_spacy"] = sentences_spacy
    table["token"] = tokens
    table["pos_treetagger"] = pos_treetagger
    table["ner_spacy"] = spacy_ner
    table["ner_flair_base"] = flair_ner_basic
    table["ner_flair_fine"] = flair_ner_large
    table["noun_chunk_spacy"] = noun_chunks
    table["noun_chunk_root_spacy"] = noun_chunks_root
    table["dependency_tag_spacy"] = spdep
    table["dependency_head_spacy"] = sphead
    table["case_marmot"] = case_marmot
    table["number_marmot"] = number_marmot
    table["gender_marmot"] = gender_marmot
    table["person_marmot"] = person_marmot
    table["tense_marmot"] = tense_marmot
    table["mood_marmot"] = mood_marmot
    table["degree_marmot"] = degree_marmot

    table.to_csv("/home/konle/DROC/DROC-Release/llp/" + filename, sep="\t")

    break