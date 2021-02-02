from commentary import Commentary
from primary_text import PrimaryText
from utils import TargetToXMLDoc

t2xml = TargetToXMLDoc()

def suggest_new_lemmas(commentary_short_name):
    """
    :param commentary_short_name: identifies a commentary file, options in code/constants
    :return:
    """
    commentary = Commentary(commentary_short_name)
    for note in commentary.notes:
        target = note.target
        lemma = note.lemma
        primary_text = PrimaryText( etree=t2xml.find_xml_root(target) )
        lemma_choices = primary_text.get_choice_dicts(target)
        print(target, lemma, primary_text, lemma_choices)


print("SEARCHING")
suggest_new_lemmas("theatre")
print("DONE")