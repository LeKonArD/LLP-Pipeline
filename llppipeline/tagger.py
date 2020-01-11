from llppipeline.base import PipelineModule

from someweta import ASPTagger
import treetaggerwrapper
import os
import subprocess
import pexpect
import sys
import re

from .util.smor_getpos import get_true_pos

class TreeTagger(PipelineModule):

    def __init__(self):
        self.tt = treetaggerwrapper.TreeTagger(TAGLANG="de")

    def targets(self):
        return {'lemma-treetagger', 'pos-treetagger'}

    def prerequisites(self):
        return {'token'}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        tagged = self.tt.tag_text(tokens, tagonly=True)
        return {
            'lemma-treetagger': [x.split("\t")[2] for x in tagged],
            'pos-treetagger': [x.split("\t")[1] for x in tagged]
        }

class SoMeWeTa(PipelineModule):

    def __init__(self, model='resources/german_newspaper_2018-12-21.model'):
        self.asptagger = ASPTagger()
        self.asptagger.load(model)

    def targets(self):
        return {'pos-someweta'}

    def prerequisites(self):
        return {'token', 'sentence'}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        sentences = prerequisite_data['sentence']

        sent_end = 0
        tagged_sentences = []

        while sent_end < len(sentences):
            sent_start = sent_end
            sent_end = sent_start
            while sent_end < len(sentences) and sentences[sent_start] == sentences[sent_end]:
                sent_end += 1

            tagged_sentences += [self.asptagger.tag_sentence(tokens[sent_start:sent_end])]

        return {
            'pos-someweta': [t[1] for sent in tagged_sentences for t in sent]
        }

class RNNTagger(PipelineModule):

    def targets(self):
        return {'pos-rnntagger', 'morphology-rnntagger', 'lemma-rnntagger'}

    def prerequisites(self):
        return {'token', 'sentence'}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        sentences = prerequisite_data['sentence']

        if not os.path.exists("temp"):
            os.mkdir("temp")

        with open("temp/rnntagger_input", 'w') as f:
            sent = sentences[0]
            for tok, s in zip(tokens, sentences):
                if s != sent:
                    f.write('\n')

                f.write(tok + '\n')
                sent = s
            f.write('\n')

        process = subprocess.run("sh ./resources/rnn-tagger-german.sh temp/rnntagger_input %s" % sys.executable,
                       shell=True, text=True, stdout=subprocess.PIPE)

        lines = process.stdout.split("\n")
        pos = []
        morph = []
        lemma = []
        for line in lines:
            if line == "":
                continue

            fields = line.split("\t")
            split = re.split("\\.", fields[1], maxsplit=1)

            if re.match('^\\$.*', fields[1]):
                pos += [fields[1]]
                morph += "_"
            else:
                pos += [split[0]]
                if len(split) > 1:
                    morph += [split[1]]
                else:
                    morph += ["_"]
            lemma += [fields[2]]

        return {'pos-rnntagger': pos, 'morphology-rnntagger': morph, 'lemma-rnntagger': lemma}


# code cited from Rico Sennrich et al.: clevertagger (https://github.com/rsennrich/clevertagger)
class Clevertagger(PipelineModule):

    def __init__(self, smor_prereq):
        self.smor_prereq = smor_prereq
        self.crf_model = './resources/hdt_ab.zmorge-20140521-smor_newlemma.model'
        self.crf_backend_exec = './resources/wapiti'

        self.alphnum = re.compile(r'^(?:\w|\d|-)+$', re.U)
        self.re_mainclass = re.compile(u'<\+(.*?)>')

    def targets(self):
        return {'pos-clevertagger'}

    def prerequisites(self):
        return {'token', 'sentence', self.smor_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        sents = prerequisite_data['sentence']
        smor = prerequisite_data[self.smor_prereq]

        tagger_args = ['label', '-m', self.crf_model]
        tagger = pexpect.spawn(self.crf_backend_exec, tagger_args, echo=False, encoding='utf-8')
        tagger.delaybeforesend = 0

        # get some initial output
        tagger.expect_exact('* Load model\r\n* Label sequences\r\n')

        # convert SMOR output to posset
        possets = list(map(lambda tags: self._convert_smor(tags), smor))

        # preprocess each sentence
        preprocessed = ['']
        sentid = sents[0]
        for i in range(len(tokens)):
            if sents[i] != sentid:
                preprocessed += ['']

            preprocessed[-1] = preprocessed[-1] + self._create_features(tokens[i], possets[i])

        # main tagging step with wapiti
        out = self._process_by_sentence(tagger, preprocessed)

        return {
            'pos-clevertagger': [line.split('\t')[14] for sentence in out for line in sentence]
        }

    def _convert_smor(self, smortags):
        posset = []
        for line in smortags:
            try:
                raw_pos = self.re_mainclass.search(line).group(1)
            except:
                continue

            pos, pos2 = get_true_pos(raw_pos, line)

            if pos:
                posset.append(pos)
            if pos2:
                posset.append(pos2)

        return posset

    def _create_features(self, word, posset):
        """Create list of features for each word"""

        pos = []

        # feature: is word uppercased?
        if word[0].isupper():
            feature_upper = 'uc'
        else:
            feature_upper = 'lc'

        # feature: is word alphanumeric?
        if self.alphnum.search(word[0]):
            feature_alnum = 'y'
        else:
            feature_alnum = 'n'

        # feature: list of possible part of speech tags
        pos = sorted(posset)+['ZZZ']*10
        posstring = '\t'.join(pos[:10])

        outstring = ("{w}\t{wlower}\t{upper}\t{alnum}\t{pos}".format(w=word, wlower=word.lower(), upper=feature_upper, pos=posstring, alnum=feature_alnum))

        return outstring+'\n'

    def _process_by_sentence(self, processor, preprocessed):
        sentences_out = []
        for sentence in preprocessed:
            if not sentence:
                continue
            words = []
            processor.send(sentence + '\n')
            while True:
                word = processor.readline().strip()
                # hack for Wapiti stderr
                if word.endswith('sequences labeled'):
                    continue
                elif word:
                    words.append(word)
                else:
                    break
            sentences_out.append(words)

        return sentences_out

