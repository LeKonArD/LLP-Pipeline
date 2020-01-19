# LLP-Pipeline
NLP Pipeline for German literary texts (under development)

## Processing Pipeline

| Name (Python class) | Requires | Provides | Notes |
| --- | --- | --- | --- |
| **Input Readers** |
| TEI parser <br> (`filereader.TEIReader`) | (XML filename) | `paragraph` | Extracts text/paragraphs from TEI-adhesive XML input. |
| Rulebased parser<br> (`filereader.Rulebased`) | (Input filename) | `paragraph` | Reads plain text files, and recognizes empty lines as paragraph break. |
| **Tokenizers** |
| SoMaJo<br> (`tokenizer.SoMaJo`) | `paragraph` | `token-somajo`, `token`, `sentence-somajo`, `sentence` | Specifically designed for social media texts. [Github](https://github.com/tsproisl/SoMaJo), [(Proisl and Uhrig 2016)](#ref-ProislUhrig2016) |
| Syntok<br> (`tokenizer.Syntok`) | `paragraph` | `token-syntok`, `token`, `sentence-syntok`, `sentence` | [Github](https://github.com/fnl/syntok) |
| **Part-of-speech taggers** |
| TreeTagger<br>(`tagger.TreeTagger`) | `token`, `sentence` | `pos-treetagger`, `lemma-treetagger` | Probabilistic tagger using decision trees. [Webpage](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/), [(Schmid, 1994)](#ref-Schmid1994) |
| SoMeWeTa<br>(`tagger.SoMeWeTa`) | `token`, `sentence` (SoMaJo tokenization recommended) | `pos-someweta` | Based on averaged structured perceptron; focuses on web and social media texts. [Github](https://github.com/tsproisl/SoMeWeTa), [(Proisl 2018)](#ref-Proisl2018) |
| RNNTagger<br>(`tagger.RNNTagger`) | `token`, `sentence` | `pos-rnntagger`, `morphology-rnntagger`, `lemma-rnntagger` | *Requires PyTorch*. Based on LSTMs. [Webpage](https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/), [(Schmid 2019)](#ref-Schmid2019) |
| Clevertagger<br>(`tagger.Clevertagger`) | `token`, `sentence`, `morphology-*` (Zmorge analysis recommended)| `pos-clevertagger` | Uses CRFs. [Github](https://github.com/rsennrich/clevertagger), [(Sennrich, Volk, Schneider 2013](#ref-SennrichtVolkSchneider2013). Uses [Wapiti](https://wapiti.limsi.fr/), [(Lavergne, Cappé, Yvon 2010)](#ref-Lavergne2010) |
| **Morphological Analyzers and Lemmatizers** |
| Zmorge<br>(`morphology.Zmorge`) | `token` | `morphology-zmorge`, `lemma-zmorge` | Based on finite-state morphological grammar SMOR. Trained on Wikitionary. [Webpage](https://pub.cl.uzh.ch/users/sennrich/zmorge/), [(Sennrich, Kunz 2014)](#ref-SennrichKunz2014)
| DEMorphy<br>(`morphology.DEMorphy`) | `token` | `morphology-demorphy` | [Github](https://github.com/DuyguA/DEMorphy/), [(Altinok 2018)](#ref-Altinok2018)
| GermaLemma<br>(`lemmatizer.GermaLemma`) | `token`, `pos-*` | `lemma-germalemma` | [Github](https://github.com/WZBSocialScienceCenter/germalemma)
| **Named Entity Recognition**
| Flair | `token` | `pos-flair`, `ner-flair` | Uses contextual string embeddings. [Github](https://github.com/flairNLP/flair), [(Akbik, Blythe, Vollgraf 2018)](#ref-AkbikBlytheVollgraf2018)
| **Full Pipelines**
| spacy | `token` | `lemma-spacy`, `pos-spacy`, `syntax-spacy`, `entity-spacy` | Uses convolutional neural network models, trained on TIGER and WikiNER. [Webpage](https://spacy.io/)
| CoreNLP | `token` | `pos-corenlp`, `syntax-corenlp`, `entities-corenlp`, `sentence-corenlp` | Uses log-linear tagger, transition-based parsing, NER using CRF models. Trained on HGC and UD-HDT. [Webpage](https://stanfordnlp.github.io/CoreNLP/), [(Manning, Surdeanu, Bauer, Finkel, Bethard,  McClosky 2014)](#ref-Manning2013)
| ParZu<br>(`parzu.Parzu`) | `token`, `sentence`, `pos-*` (Clevertagger recommended), `morphology-*` (Zmorge analysis recommended)| `syntax-parzu` | Hybrid architecture using hand-written rules and statistical disambiguation. Trained on TüBa-D/Z.  [Github](https://github.com/rsennrich/ParZu), [(Sennrich, Volk, Schneider 2013](#ref-SennrichtVolkSchneider2013) |

## Evaluation
## Analysis Tools

## Requirements
* python >= 3.7
  * see `requirements.txt` for required packages
  
## Installation

## References

<div id="refs" class="references">

<div id="ref-AkbikBlytheVollgraf2018">

Akbik, Alan, Duncan Blythe, and Roland Vollgraf. 2018. "Contextual
String Embeddings for Sequence Labeling." In *COLING 2018, 27th
International Conference on Computational Linguistics*, 1638--49.
Association for Computational Linguistics.

</div>

<div id="ref-Altinok2018">

Altinok, Duygu. 2018. "DEMorphy, German Language Morphological
Analyzer." <https://arxiv.org/abs/1803.00902>.

</div>

<div id="ref-Lavergne2010">

Lavergne, Thomas, Olivier Cappé, and François Yvon. 2010. "Practical
Very Large Scale CRFs." In *Proceedings the 48th Annual Meeting of the
Association for Computational Linguistics (ACL)*, 504--13. Uppsala,
Sweden: Association for Computational Linguistics.
<http://www.aclweb.org/anthology/P10-1052>.

</div>

<div id="ref-Manning2013">

Manning, Christopher D., Mihai Surdeanu, John Bauer, Jenny Finkel,
Steven J. Bethard, and David McClosky. 2014. "The Stanford CoreNLP
Natural Language Processing Toolkit." In *Proceedings of 52nd Annual
Meeting of the Association for Computational Linguistics: System
Demonstrations*, 55--60. Baltimore, Maryland: Association for
Computational Linguistics.
<http://www.aclweb.org/anthology/P/P14/P14-5010>.

</div>

<div id="ref-Proisl2018">

Proisl, Thomas. 2018. "SoMeWeTa: A Part-of-Speech Tagger for German
Social Media and Web Texts." In *Proceedings of the Eleventh
International Conference on Language Resources and Evaluation (LREC
2018)*, 665--70. Miyazaki, Japan: European Language Resources
Association ELRA.
<http://www.lrec-conf.org/proceedings/lrec2018/pdf/49.pdf>.

</div>

<div id="ref-ProislUhrig2016">

Proisl, Thomas, and Peter Uhrig. 2016. "SoMaJo: State-of-the-Art
Tokenization for German Web and Social Media Texts." In *Proceedings of
the 10th Web as Corpus Workshop (WAC-X) and the EmpiriST Shared Task*,
57--62. Berlin, Germany: Association for Computational Linguistics
(ACL). <http://aclweb.org/anthology/W16-2607>.

</div>

<div id="ref-Schmid1994">

Schmid, Helmut. 1994. "Probabilistic Part-of-Speech Tagging Using
Decision Trees." In *Proceedings of International Conference on New
Methods in Language Processing*. Manchester, UK.
<https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger1.pdf>.

</div>

<div id="ref-Schmid2019">

Schmid, Helmut. 2019. "Deep Learning-Based Morphological Taggers and
Lemmatizers for Annotating Historical Texts." In *DATeCH, Proceedings of
the 3rd International Conference on Digital Access to Textual Cultural
Heritage*, 133--37. Brussels, Belgium: Association for Computing
Machinery.
<https://www.cis.uni-muenchen.de/~schmid/papers/Datech2019.pdf>.

</div>

<div id="ref-SennrichKunz2014">

Sennrich, Rico, and Beat Kunz. 2014. "Zmorge: A German Morphological
Lexicon Extracted from Wiktionary." In *Proceedings of the Ninth
International Conference on Language Resources and Evaluation
(Lrec'14)*. Reykjavik, Iceland: European Language Resources Association
(ELRA).

</div>

<div id="ref-SennrichtVolkSchneider2013">

Sennrich, Rico, Martin Volk, and Gerold Schneider. 2013. "Exploiting
Synergies Between Open Resources for German Dependency Parsing,
POS-Tagging, and Morphological Analysis." In *Proceedings of the
International Conference Recent Advances in Natural Language Processing
RANLP 2013*, 601--9. Hissar, Bulgaria: INCOMA Ltd.
<https://www.aclweb.org/anthology/R13-1079>.

</div>


</div>
