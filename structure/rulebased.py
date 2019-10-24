import re


def split_chapters(raw_text):

    splitted_paragraphs = re.split("\n{8}", raw_text)

    return splitted_paragraphs


def split_paragraphs(raw_text):
    
    splitted_paragraphs = re.split("\n{4}", raw_text)
    
    return splitted_paragraphs


def split_paragraphs_in_chapter(chapters):

    splitted_paragraphs = [re.split("\n{4}", chapter) for chapter in chapters]

    return splitted_paragraphs
