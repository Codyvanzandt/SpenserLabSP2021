from lxml import etree
from constants import NSMAP
from utils import load_primary_xml, yield_all_xml_roots
import os
import itertools



class PrimaryTexts:

    def __init__(self):
        self.xml = self.build_composite_primary_xml()

    def build_composite_primary_xml(self):
        composite_xml = etree.Element("composite")
        for root in yield_all_xml_roots():
            composite_xml.append(root)
        return composite_xml

    def get_reference_nodes(self, target):
        return self.xml.xpath(f'//tei:ref[@n="{target}"]', namespaces=NSMAP)

    def get_choice_nodes(self, target):
        references_nodes = self.get_reference_nodes(target)
        return list(
            itertools.chain.from_iterable(
                [reference_node.xpath(f'.//tei:choice', namespaces=NSMAP) for reference_node in references_nodes]
            )
        )

    def get_alternate_spellings(self, target):
        choice_nodes = self.get_choice_nodes(target)
        normal_to_oxford = dict()
        for choice_node in choice_nodes:
            normal = choice_node.xpath(f'.//tei:reg', namespaces=NSMAP)[0].text
            oxford = choice_node.xpath(f'.//tei:orig', namespaces=NSMAP)[0].text
            normal_to_oxford[normal] = oxford
        return normal_to_oxford

    def xpath(self, *args, **kwargs):
        kwargs["namespaces"] = NSMAP
        return self.xml.xpath(*args, **kwargs)

# target = "theatre_1347642000450"
# pt = PrimaryTexts()
#
# print(pt.get_reference_nodes(target))
# print(pt.get_choice_nodes(target))
# print(pt.get_choice_dicts(target))
