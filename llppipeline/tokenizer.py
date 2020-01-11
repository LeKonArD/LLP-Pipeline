from somajo import SoMaJo
import syntok.segmenter

from llppipeline.base import PipelineModule

class SoMaJo(PipelineModule):

    def targets(self):
        return {'token-somajo', 'sentence-somajo', 'token', 'sentence'}

    def prerequisites(self):
        return {'paragraph'}

    def make(self, prerequisite_data):
        paragraphs = prerequisite_data['paragraph']
        tokenizer = SoMaJo("de_CMC", split_camel_case=True)
        sentences = tokenizer.tokenize_text(paragraphs)

        tokens = []
        sentence_alignment = []

        for (i, s) in zip(range(len(sentences)), sentences):
            tokens += [token.text for token in s]
            sentence_alignment += [i] * len(s)

        return {'token-somajo': tokens, 'sentence-somajo': sentence_alignment, 'token': tokens, 'sentence': sentence_alignment}


class Syntok(PipelineModule):

    def targets(self):
        return {'token-syntok', 'sentence-syntok', 'token', 'sentence'}

    def prerequisites(self):
        return {'paragraph'}

    def make(self, prerequisite_data):
        paragraphs = prerequisite_data['paragraph']
        tokens = []
        sentence_alignment = []
        sent_num = 0

        for para in paragraphs:
            sentences = [sent for p in syntok.segmenter.process(para) for sent in p]
            for s in sentences:
                tokens += [token.value for token in s]
                sentence_alignment += [sent_num] * len(s)
                sent_num = sent_num + 1

        return {'token-syntok': tokens, 'sentence-syntok': sentence_alignment, 'token': tokens, 'sentence': sentence_alignment}
