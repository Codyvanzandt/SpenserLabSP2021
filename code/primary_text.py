from lxml import etree
from constants import NSMAP
from utils import load_primary_xml
import os
import itertools



class PrimaryText:

    def __init__(self, file_name=None, etree=None):
        self.file_name = file_name
        self.xml = etree if etree is not None else load_primary_xml(file_name)

    def __repr__(self):
        return f"{self.__class__.__name__}( file_name={repr(self.file_name)} )"

    def get_reference_nodes(self, target):
        return self.xml.xpath(f'//tei:ref[@n="{target}"]', namespaces=NSMAP)

    def get_choice_nodes(self, target):
        references_nodes = self.get_reference_nodes(target)
        return list(
            itertools.chain.from_iterable(
                [reference_node.xpath(f'.//tei:choice', namespaces=NSMAP) for reference_node in references_nodes]
            )
        )

    def get_choice_dicts(self, target):
        choice_nodes = self.get_choice_nodes(target)
        choice_dict = dict()
        for choice_node in choice_nodes:
            normal = choice_node.xpath(f'.//tei:reg', namespaces=NSMAP)[0].text
            oxford = choice_node.xpath(f'.//tei:orig', namespaces=NSMAP)[0].text
            choice_dict[normal] = oxford
        return choice_dict

# letters_tp1 = "1_theatre_div_type_commendatory_poems_.xml"
# target = "theatre_1347642000450"
# pt = PrimaryText(file_name=letters_tp1)
#
# print(pt.get_reference_nodes(target))
# print(pt.get_choice_nodes(target))
# print(pt.get_choice_dicts(target))
