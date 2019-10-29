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


# Run a test with all available Features
# set path to input plain text
input = "test_file.txt"

# set output path
output = "test_ouput.tsv"

# set tokenizer (list); since tokenization is crucial for every following step,
# one output for every tokenizer will be generated
# possible choices: "spacy","somajo","treetagger"

tokenizers = ["treetagger"]


input_text = open(input, "r").read()

for tokenizer_choice in tokenizers:

    if tokenizer_choice == "spacy":

        # structure
        chapters = split_chapters(input_text)
        chapters = split_paragraphs_in_chapter(chapters)

        # tokenizer
        tokens = token_sp(chapters)

        # structure/tokenizer alignment
        chap, para, tokens = align_token_structure(tokens)

    if tokenizer_choice == "treetagger":

        # structure
        chapters = split_chapters(input_text)
        chapters = split_paragraphs_in_chapter(chapters)

        # tokenizer
        tokens = token_tt(chapters)

        # structure/tokenizer alignment
        chap, para, tokens = align_token_structure(tokens)

    if tokenizer_choice == "somajo":

        # structure
        chapters = split_chapters(input_text)
        chapters = split_paragraphs_in_chapter(chapters)

        # tokenizer
        tokens = token_smo(chapters)

        # structure/tokenizer alignment
        chap, para, tokens = align_token_structure(tokens)

    # sentence splitter
    sentences_spacy = sent_sp(tokens)
    sentences_smo = sent_smo(tokens)
    sentences_smo = align_token_sentence(sentences_smo)
    # morphology
    case_marmot, number_marmot, gender_marmot, person_marmot, tense_marmot, mood_marmot, degree_marmot = morph_marmot(tokens, sentences_smo)

    # pos tagger
    pos_treetagger = tagpos_tt(tokens)
    pos_spacy = tagpos_sp(tokens)
    pos_flair_basic = flair_pos_base(tokens)
    #pos_flair_fine = flair_pos_fine(tokens)
    #needs a modelfile and a bit of RAM
    #pos_someweta = smwt_pos(tokens)

    # lemmatizer
    lemma_treetagger = lemma_tt(tokens)
    # this needs tiger corpus
    # lemma_gemrmalemma = lemma_gl(tokens)

    # chunker
    noun_chunks, noun_chunks_root = nounchunk_sp(tokens)

    # dependency
    spdep, sphead = spdep(tokens)
    
    # NER
    spacy_ner = sp_ner(tokens)
    flair_ner_basic = flair_ner_base(tokens)
    flair_ner_large = flair_ner_fine(tokens)
    
    
    # output creation
    table = pd.DataFrame()
    table["chapter"] = chap
    table["paragraphs"] = para
    table["sentence_spacy"] = sentences_spacy
    table["sentence_smo"] = sentences_smo
    table["token"] = tokens
    table["pos_treetagger"] = pos_treetagger
    table["pos_spacy"] = pos_spacy
    table["pos_flair_base"] = pos_flair_basic
    #table["pos_flair_fine"] = pos_flair_fine
    table["ner_spacy"] = spacy_ner
    table["ner_flair_base"] = flair_ner_basic
    table["ner_flair_fine"] = flair_ner_large
    #table["pos_someweta"] = pos_someweta
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

    table.to_csv(tokenizer_choice+"_"+output, sep="\t")
