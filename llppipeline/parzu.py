import sys
import os
import pexpect
import codecs
import re
import tempfile

from llppipeline.base import PipelineModule
from resources.parzu.preprocessor.treetagger2prolog import format_conversion
from resources.parzu.preprocessor.morphology.morphisto2prolog import main as morphisto2prolog
from resources.parzu.postprocessor.cleanup_output import cleanup_conll

# cited from Sennrich et al.: https://github.com/rsennrich/parzu
class Parzu(PipelineModule):

    def __init__(self, pos_prereq, smor_prereq):
        self.pos_prereq = pos_prereq
        self.smor_prereq = smor_prereq

        # launch morphological preprocessing (prolog script)
        self.prolog_preprocess = pexpect.spawn('swipl',
                                               ['-q', '-s', 'resources/parzu/preprocessor/preprocessing.pl'],
                                               echo=False,
                                               #logfile=sys.stderr,
                                               timeout=None,
                                               encoding='utf-8')

        self.prolog_preprocess.expect_exact('?- ')
        self.prolog_preprocess.delaybeforesend = 0

        # launch main parser process (prolog script)
        self.prolog_parser = pexpect.spawn('swipl',
                                           ['-q', '-s', 'ParZu-parser.pl', '-G248M', '-L248M'],
                                           echo=False,
                                           #logfile=sys.stderr,
                                           encoding='utf-8',
                                           timeout=None,
                                           cwd='resources/parzu/core')

        self.prolog_parser.expect_exact('?- ')
        self.prolog_parser.delaybeforesend = 0

        # initialize parser parameters
        parser_init = "retract(sentdelim(_))," \
                      + "assert(sentdelim('$newline'))," \
                      + "retract(returnsentdelim(_))," \
                      + "assert(returnsentdelim(no))," \
                      + "retract(nbestmode(_))," \
                      + "assert(nbestmode(0))," \
                      + 'retractall(morphology(_)),' \
                      + "assert(morphology(gertwol))," \
                      + "retractall(lemmatisation(_))," \
                      + "assert(lemmatisation(gertwol))," \
                      + "retractall(extrainfo(_))," \
                      + "assert(extrainfo(no))," \
                      + "start_german."

        self.prolog_parser.sendline(parser_init)
        self.prolog_parser.expect('.*\?- ')


    def targets(self):
        return {'syntax-parzu'}

    def prerequisites(self):
        return {'token', 'sentence', self.pos_prereq, self.smor_prereq}

    def make(self, prerequisite_data):
        tokens = prerequisite_data['token']
        analyses = []
        for token,analysis in zip(tokens, prerequisite_data[self.smor_prereq]):
            analyses.append("> " + token)
            analyses.extend(filter(lambda a: a.strip() != '', analysis))

        sent_alignment = prerequisite_data['sentence']
        sent_end = 0
        sentences = []
        while sent_end < len(sent_alignment):
            sent_start = sent_end
            sent_end = sent_start
            while sent_end < len(sent_alignment) and sent_alignment[sent_start] == sent_alignment[sent_end]:
                sent_end += 1

            sentence = '\n'.join([token+'\t'+pos for token,pos in zip(tokens[sent_start:sent_end], prerequisite_data[self.pos_prereq][sent_start:sent_end])])
            sentences.append(sentence)

        preprocessed_file = self.preprocess(sentences, analyses)
        outfile = self.parse(preprocessed_file)

        output = list(cleanup_conll(codecs.open(outfile.name, encoding='UTF-8')))

        syntax = []
        for sent in output:
            tokenidx = 0
            for line in sent.split('\n'):
                tokenidx = tokenidx + 1

                if line.strip() == '':
                    continue

                rel = line.split('\t')[7]
                if rel == 'root':
                    head = 0
                else:
                    head = int(line.split('\t')[6]) - tokenidx

                syntax.append((rel, head))

        os.remove(preprocessed_file.name)
        os.remove(outfile.name)

        return {
            'syntax-parzu': syntax
        }

    #convert to prolog-readable format
    #identify verb complexes
    #input: list of sentences, morphological analyses
    def preprocess(self, sentences, analyses):

        # convert to prolog format and get vocabulary
        sentences_out = []
        for sentence in sentences:
            sentence_out = []
            for line in sentence.splitlines():
                word, line = format_conversion(line)
                sentence_out.append(line)

            sentence_out.append("w('ENDOFSENTENCE','$newline',['._$newline'],'ENDOFSENTENCE').")

            sentences_out.append('\n'.join(sentence_out))

        sentences_out.append("\nw('ENDOFDOC','$newline',['._$newline'],'ENDOFDOC').")

        # convert morphological analysis to prolog format
        analyses = morphisto2prolog(analyses)

        #having at least one entry makes sure that the preprocessing script doesn't crash
        analyses.append('gertwol(\'<unknown>\',\'<unknown>\',_,_,_).')

        # communication with swipl scripts is via temporary files
        preprocessed_file = tempfile.NamedTemporaryFile(prefix="ParZu-preprocessed.pl", delete=False, dir="temp")
        morph_file = tempfile.NamedTemporaryFile(prefix="ParZu-morph.pl", delete=False, dir="temp")
        tag_file = tempfile.NamedTemporaryFile(prefix="ParZu-tag.pl", delete=False, dir="temp")
        preprocessed_file.close()
        morph_file.close()
        tag_file.close()
        codecs.open(morph_file.name, 'w', encoding='UTF-8').write('\n'.join(analyses))
        codecs.open(tag_file.name, 'w', encoding='UTF-8').write('\n'.join(sentences_out))

        # start preprocessing script and wait for it to finish
        self.prolog_preprocess.sendline(
            "retractall(gertwol(_,_,_,_,_)),"
            "retractall(lemmatisation(_)),"
            "retractall(morphology(_)),"
            "assert(lemmatisation(smor)),"
            "assert(morphology(smor)),"
            "retract(sentdelim(_)),"
            "assert(sentdelim('$newline')),"
            "start('"+morph_file.name+"','"+tag_file.name+"','"+preprocessed_file.name+"').")

        while True:
            line = self.prolog_preprocess.readline()
            line = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)
            if re.match('(\?-\s)?true\.\r\n', line):
                break

        os.remove(morph_file.name)
        os.remove(tag_file.name)
        return preprocessed_file

    #main parsing step
    def parse(self, preprocessed_file):
        parsed_file = tempfile.NamedTemporaryFile(prefix="ParZu-parsed.pl", delete=False, dir="temp")
        parsed_file.close()

        cmd = "retract(outputformat(_))," \
              + "assert(outputformat(conll))," \
              + "go_textual('"+os.path.abspath(preprocessed_file.name)+"', '"+os.path.abspath(parsed_file.name)+"').\n"

        self.prolog_parser.sendline(cmd)

        while True:
            line = self.prolog_parser.readline()
            line = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)     # remove styling tokens
            if re.match('(\?-)?(\s+\|\s+)?true\.\r\n', line):
                break

        return parsed_file
