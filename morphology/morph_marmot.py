import subprocess
import re
import pandas as pd

def get_field_marmot(field_pattern, field, text):

    text = str(text)
    if field_pattern.match(text):

        value = re.sub(".*"+field+"=", "", text)
        value = re.sub("\|.*", "", value)

        return value

    else:

        return "O"

def parse_marmot(output):

    case = list(output.iloc[:, 7].apply(lambda x: get_field_marmot(re.compile(".*case"), "case", x)))
    number = list(output.iloc[:, 7].apply(lambda x: get_field_marmot(re.compile(".*number"), "number", x)))
    gender = list(output.iloc[:, 7].apply(lambda x: get_field_marmot(re.compile(".*gender"), "gender", x)))
    person = list(output.iloc[:, 7].apply(lambda x: get_field_marmot(re.compile(".*person"), "person", x)))
    tense = list(output.iloc[:, 7].apply(lambda x: get_field_marmot(re.compile(".*tense"), "tense", x)))
    mood = list(output.iloc[:, 7].apply(lambda x: get_field_marmot(re.compile(".*mood"), "mood", x)))
    degree = list(output.iloc[:, 7].apply(lambda x: get_field_marmot(re.compile(".*degree"), "degree", x)))

    return case, number, gender, person, tense, mood, degree

def morph_marmot(tokens, sents):

    tmp_file = ""
    sent_id = sents[0]
    i = 1
    for token in tokens:
        tmp_file += token+"\n"

        if i == len(sents):
            continue

        if sents[i] != sent_id:
            tmp_file += "\n"
            sent_id = sents[i]

        i += 1

    with open("tmpfile.txt", "w") as f:
        f.write(tmp_file)


    process = subprocess.Popen("java -cp models/marmot-2019-10-28.jar marmot.morph.cmd.Annotator --model-file models/de.marmot --test-file form-index=0,tmpfile.txt --pred-file tmp_out.txt", shell=True)
    process.wait()

    output = pd.read_csv("tmp_out.txt", sep="\t", header=None)
    case, number, gender, person, tense, mood, degree = parse_marmot(output)
    return case, number, gender, person, tense, mood, degree
