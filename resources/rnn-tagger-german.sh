#!/bin/sh

INPUT=$(realpath $1)

cd "$(dirname "$0")/RNNTagger"

PYTHON=${2:-python}
BIN=./bin
SCRIPTS=./scripts
LIB=./lib
PyRNN=./PyRNN
PyNMT=./PyNMT
TMP=../../temp/rnn-tagger
LANGUAGE=german

TOKENIZER=${SCRIPTS}/tokenize.pl
ABBR_LIST=${LIB}/Tokenizer/${LANGUAGE}-abbreviations
TAGGER=$PyRNN/rnn-annotate.py
RNNPAR=${LIB}/PyRNN/${LANGUAGE}
REFORMAT=${SCRIPTS}/reformat.pl
LEMMATIZER=$PyNMT/nmt-translate.py
NMTPAR=${LIB}/PyNMT/${LANGUAGE}

# $TOKENIZER -g -a $ABBR_LIST $INPUT > $TMP.tok
$PYTHON $TAGGER $RNNPAR $INPUT > $TMP.tagged
$REFORMAT $TMP.tagged > $TMP.reformatted
$PYTHON $LEMMATIZER --print_source $NMTPAR $TMP.reformatted > $TMP.lemmas
$SCRIPTS/lemma-lookup.pl $TMP.lemmas $TMP.tagged 
