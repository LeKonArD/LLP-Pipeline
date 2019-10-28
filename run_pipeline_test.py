from structure.rulebased import split_paragraphs, split_chapters, split_paragraphs_in_chapter
from tokenizers.toksomajo import token_smo
from tokenizers.tok_alignment import align_token_structure
from sentence.sentsomajo import sent_smo
from sentence.sent_alignment import align_token_sentence
from postagger.spacy_tagpos import tagpos_sp
from tokenizers.toktreetagger import token_tt
from tokenizers.tokspacy import token_sp
from postagger.tt_tagpos import tagpos_tt
from sentence.sentspacy import sent_sp
from chunker.sp_nounchunks import nounchunk_sp
from lemmatizer.tt_lemma import lemma_tt
#from lemmatizer.germalemma import gl_lemma
from postagger.someweta_pos import smwt_pos
from NER.nerspacy import sp_ner
from NER.nerflair import flair_ner_base
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

    # pos tagger
    pos_treetagger = tagpos_tt(tokens)
    pos_spacy = tagpos_sp(tokens)
    #needs a modelfile and a bit of RAM
    #pos_someweta = smwt_pos(tokens)

    # lemmatizer
    lemma_treetagger = lemma_tt(tokens)
    # this needs tiger corpus
    # lemma_gemrmalemma = lemma_gl(tokens)

    # chunker
    noun_chunks, noun_chunks_root = nounchunk_sp(tokens)

    # NER
    spacy_ner = sp_ner(tokens)
    flair_ner1 = flair_ner_base(tokens)
    
    
    # output creation
    table = pd.DataFrame()
    table["chapter"] = chap
    table["paragraphs"] = para
    table["sentence_spacy"] = sentences_spacy
    table["sentence_smo"] = sentences_smo
    table["token"] = tokens
    table["pos_treetagger"] = pos_treetagger
    table["pos_spacy"] = pos_spacy
    table["ner_spacy"] = spacy_ner
    table["ner_flair_base"] = flair_ner1
    #table["pos_someweta"] = pos_someweta
    table["noun_chunk_spacy"] = noun_chunks
    table["noun_chunk_root_spacy"] = noun_chunks_root

    table.to_csv(tokenizer_choice+"_"+output, sep="\t")
