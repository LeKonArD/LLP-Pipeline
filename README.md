# LLP-Pipeline
NLP Pipeline for German literary texts (under development)
## Structure
### Paragraphs
* TEI Parser (not yet)
* Rule based (done)
### Chapters
* TEI Parser (not yet)
* Rule based (done)
## Tokenization
* TreeTagger (done)
* SoMaJo (done)
* Flair (==segtok==nicht geeignet, not yet)
* spaCy (done, + remove linebreaks)
## Chunking
* spaCy (done)
## Sentence Splitting
* SpaCy (done)
* SoMaJo (done)
* Flair (not yet, siehe Tokenizer)
## Lemmatization
* TreeTagger (done)
* RNNTagger (not yet)
* GermaLemma (done)
* SMORLemma (not yet)
* spaCy (too bad)
## Part-of-Speech Tagger
* TreeTagger (done)
* RNNTagger (not yet)
* clevertagger (not yet)
* spacy (done)
* SoMeWeTa (done, get model: <a href="https://github.com/tsproisl/SoMeWeTa#model-files">link</a>)
* StanfordNLP (not yet)
## Morphological Tagger
* DEMorphy (not yet, python<3.7, but flair python>=3.7)
## Named Entity Recognition (fine-grained)
* Flair (done)
* S. Pado NER (not yet)
## Dependency Parsing
* spacy (not yet)
* parZu (not yet)
* StanfordNLP (not yet)
* Parsey McPasresface (not yet)
## Semantic Role Labeling
* mateplus (not yet)
## Corefence Resolution
* CorZu (not yet)
# Evaluation
# Analysis Tools
# Requirements
TreeTagger <br>
python >= 3.7
* spacy
* treetaggerwrapper
* pandas
* SoMeWeTa
* SoMaJo
* germalemma
* flair
