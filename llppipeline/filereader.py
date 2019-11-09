from llppipeline.base import PipelineModule
from lxml import etree
import re

class PlainReader(PipelineModule):

    def __init__(self, input_file, para_separator = "\n\n+"):
        self.input_file = input_file
        self.para_separator = para_separator

    def targets(self):
        return {'paragraph'}

    def prerequisites(self):
        return {}

    def make(self, prerequisite_data):
        with open(self.input_file) as f:
            raw_text = f.read()
            paras = re.split(self.para_separator, raw_text)

            return {'paragraph': paras}

class TEIReader(PipelineModule):

    def __init__(self, input_file, chaptype = "chapter"):
        self.chaptype = chaptype
        self.input_file = input_file

    def targets(self):
        return {'paragraph'}

    def prerequisites(self):
        return {}

    def make(self, prerequisite_data):
        # TODO remove chapter support?
        tree = etree.parse(self.input_file)
        _strip_ns_prefix(tree)
        context = etree.iterwalk(tree.getroot(), events=("start", "end"))

        struct = []
        cur_chap = []
        cur_par = ""

        for action, elem in context:
            if elem.tag == 'teiHeader':
                context.skip_subtree()
                continue

            if action == 'start' and re.match('div[0-9]?', elem.tag) and elem.get('type') == self.chaptype:
                if cur_par != "":
                    cur_chap += [cur_par]
                    cur_par = ""
                if len(cur_chap) != 0:
                    struct += [cur_chap]
                    cur_chap = []

            if action == 'start' and elem.tag == 'p':
                if cur_par != "":
                    cur_chap += [cur_par]
                    cur_par = ""

            if action == 'start' and is_text_el(elem) and elem.text:
                cur_par += elem.text

            if action == 'end' and is_text_el(elem) and elem.tail:
                cur_par += elem.tail

        if cur_par != "":
            cur_chap += [cur_par]
        if len(cur_chap) != 0:
            struct += [cur_chap]

        return struct


def is_text_el(el):
    return re.match("abbr|addrLine|address|date|distinct|emph|foreign|head|headItem|headLabel|hi|item|l|label|lg|list|measure|name|num|p|q|rs|said|sic|soCalled|sp|stage|term|textLang|time|title|unclear|unit", el.tag) != None

def _strip_ns_prefix(tree):
    namespaces = tree.getroot().nsmap.values()

    #xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    #for each element returned by the above xpath query...
    for element in tree.xpath(query):
        #replace element name with its local name
        element.tag = etree.QName(element).localname
    return namespaces, tree
