#!/bin/sh

INPUT=$(realpath $2)
TASK=$1

cd "$(dirname "$0")/RNNTagger"

PYTHON=${3:-python}
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

if [ $TASK = 'tag' ]; then
  $PYTHON $TAGGER $RNNPAR $INPUT 2>/dev/null
fi

if [ $TASK = 'lemmatize' ]; then
  sed '/^$/d;s/\(.\)/\1 /g;s/   / <> /g;s/\t/ ## /g;' $INPUT \
    | $PYTHON $LEMMATIZER --print_source $NMTPAR /dev/stdin 2>/dev/null \
    | sed '/##/d;/^$/d;s/ //g;s/<>/ /g'
fi
