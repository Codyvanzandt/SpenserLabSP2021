from commentary import Commentary
from primary_text import PrimaryTexts
from lxml import etree

def suggest_new_lemmas(commentary_short_name):
    """
    :param commentary_short_name: identifies a commentary file, options in code/constants
    :return:
    """
    primary_texts = PrimaryTexts()
    commentary = Commentary(commentary_short_name)
    for note in commentary.notes:
        target = note.target
        lemmas = note.lemmas
        normal_to_oxford_spelling = primary_texts.get_alternate_spellings(target)
        # print(f"{target}\t{lemmas}\t{normal_to_oxford_spelling}")


# print("SEARCHING")
# suggest_new_lemmas("theatre")
# print("DONE")