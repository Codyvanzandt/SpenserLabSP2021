import os
import re
from lxml import etree
from constants import NSMAP, COMMENTARY_SHORT_NAMES
from utils import load_commentary_xml


class Commentary:
    def __init__(self, commentary_short_name):
        self.commentary_short_name = commentary_short_name
        self.xml_tree = load_commentary_xml(COMMENTARY_SHORT_NAMES[self.commentary_short_name])
        self.notes = list(map( CommentaryNote, self.xml_tree.xpath("//tei:note", namespaces=NSMAP) ) )

    def __repr__(self):
        return f'{self.__class__.__name__}( commentary_short_name={repr(self.commentary_short_name)} )'

class CommentaryNote:
    def __init__(self, note_node):
        self.target = self.get_target(note_node)
        self.target_end = self.get_target_end(note_node)
        self.note_type = self.get_type(note_node)
        self.lemma = self.get_lemma(note_node)
        self.note_text = self.get_text(note_node)

    def __repr__(self):
        return f'{self.__class__.__name__}( target={repr(self.target)}, target_end={repr(self.target_end)}, note_type={repr(self.note_type)}, lemma={repr(self.lemma)}, note_text={repr(self.note_text)} )'

    def get_target(self, note_node):
        """
        :param note_node: a note Element
        :return: the value of the target attribute

        This function assumes target exists. It will fail if it does not.
        """
        return self.remove_target_prefix_suffix( note_node.get("target") )

    def get_target_end(self, note_node):
        """
        :param note_node: a note Element
        :return: the value of the targetEnd attribute, if one exists

        Not every <note> has a targetEnd attribute; this function tries to gracefully handle that case.
        Furthermore, the targetEnd values need to be stripped of prefixes and suffixes
        to be compatible with the primary text files.
        """
        target_end = note_node.get("targetEnd")
        return self.remove_target_prefix_suffix(target_end) if target_end else None

    @staticmethod
    def remove_target_prefix_suffix(target):
        return re.search(r"^#([^_]+_\d+)",target).group(1)

    @staticmethod
    def get_lemma(note_node):
        """
        :param note_node: a note Element
        :return: the lemma associated with note_node's enclosed <mentioned> tag

        Lemmas are sometimes <mentioned> text, other times <mentioned><span> text.
        Not every <note> has an enclosed <mentioned>; this function tries to gracefully handle all this.
        """
        mentioned_list = note_node.xpath(".//tei:mentioned", namespaces=NSMAP)
        if mentioned_list:
            mention = mentioned_list[0]
            return  ''.join(mention.itertext())

    @staticmethod
    def get_text(note_node):
        """
        :param note_node: a note Element
        :return: the note's text, which tails the note's enclosed <mentioned>
        """
        mentioned_list = note_node.xpath(".//tei:mentioned", namespaces=NSMAP)
        if len(mentioned_list) == 1:
            return mentioned_list[0].tail
        else:
            return None

    @staticmethod
    def get_type(note_node):
        """
        :param note_node: a note Element
        :return: the note's type
        """
        return note_node.get("type")
