#!/bin/sh
#set -e

WGET="wget -nc"
cd "$(dirname "$0")"

#
# SoMeWeTa
#
$WGET 'http://corpora.linguistik.uni-erlangen.de/someweta/german_newspaper_2018-12-21.model'

#
# GermaLemma
#
$WGET 'https://www.ims.uni-stuttgart.de/documents/ressourcen/korpora/TIGERCorpus/download/tigercorpus-2.2.conll09.tar.gz'
if [ ! -f "tiger_release_aug07.corrected.16012013.conll09" ]; then
    tar xvf 'tigercorpus-2.2.conll09.tar.gz'
fi

#
# TreeTagger
#
$WGET 'https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.2.tar.gz'
$WGET 'https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz'
$WGET 'https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german.par.gz'
mkdir treetagger
tar -C treetagger -xvf tree-tagger-linux-3.2.2.tar.gz
tar -C treetagger -xvf tagger-scripts.tar.gz
gunzip -c german.par.gz > treetagger/german.par

#
# marmot
#
$WGET 'http://cistern.cis.lmu.de/marmot/bin/CURRENT/marmot-2015-10-22.jar'
$WGET 'http://cistern.cis.lmu.de/marmot/models/CURRENT/spmrl/de.marmot'

#
# SFST Transducer, Zmorge
# 
$WGET 'https://www.cis.uni-muenchen.de/~schmid/tools/SMOR/data/SMOR-linux.tar.gz'
$WGET 'https://pub.cl.uzh.ch/users/sennrich/zmorge/transducers/zmorge-20150315-smor_newlemma.ca.zip'
if [ ! -f "fst-infl2" ]; then
    tar xvf SMOR-linux.tar.gz --strip-components 2 SMOR/bin/fst-infl2
fi
if [ ! -f "zmorge-20150315-smor_newlemma.ca" ]; then
    unzip 'zmorge-20150315-smor_newlemma.ca.zip'
fi

#
# CoreNLP
#
$WGET 'http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip'
unzip -uo 'stanford-corenlp-full-2018-10-05.zip'
$WGET 'http://nlp.stanford.edu/software/stanford-german-corenlp-2018-10-05-models.jar' -O 'stanford-corenlp-full-2018-10-05/stanford-german-corenlp-2018-10-05-models.jar'

#
# RNNTagger
#
$WGET 'https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/data/RNNTagger.zip'
unzip -uo 'RNNTagger.zip'

#
# ParZu
#
git clone https://github.com/rsennrich/ParZu parzu
cd parzu
git checkout ed0e71c
cd ..


sha256sum -c sha256sums
