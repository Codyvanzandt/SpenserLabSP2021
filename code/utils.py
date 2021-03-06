import os
from lxml import etree

# Loading XML as an LXML etree

def load_primary_xml(file_name):
    with open(os.path.join("data", "easier_primary_texts", file_name), "rb") as xml_file:
        return etree.fromstring(xml_file.read())

def load_commentary_xml(file_name):
    with open(os.path.join("data", "commentary", file_name), "rb") as xml_file:
        return etree.fromstring(xml_file.read())


# concatenating all primary text xml into a single tree

def yield_all_xml_roots():
    for file in os.listdir(os.path.join("data", "easier_primary_texts")):
        full_path = os.path.join("data", "easier_primary_texts", file)
        with open(full_path, "rb") as xml_file:
            yield etree.fromstring(xml_file.read())
