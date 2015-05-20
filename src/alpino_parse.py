# functions used to parse and analyze the given questions

import socket
from lxml import etree
from exception_classes import *

def parse_question(question, host='zardoz.service.rug.nl', port=42424):
    """
    Analyseert de gestelde vraag tot op het niveau van het concept en de eigenschap in natuurlijke taal, met hulp van
    Alpino voor het parsen van de vraag.

    :param question: De door de gebruiker gestelde vraag als string.
    :return: de parse als XML.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    question += "\n\n"
    question_bytes = question.encode('utf-8')
    s.sendall(question_bytes)
    bytes_received = b''
    while True:
        byte = s.recv(8192)
        if not byte:
            break
        bytes_received += byte
    xml = etree.fromstring(bytes_received)
    return xml

def analyze_question(xml):
    """
    Probeert concept en eigenschap uit een vraag in natuurlijke taal te filteren met behulp van een parse van Alpino.

    :param parsed_q: de parse uit Alpino in XML.
    :return: het concept en de bijbehorende eigenschap in een Tuple.
    """
    # TODO: Uitbreiden verkrijgen concept
    identity = []
    names = xml.xpath('//node[@rel="obj1" and @ntype="eigen"] | //node[@spectype="deeleigen"] | //node[@rel="su" and @ntype="eigen"]')
    for name in names:
        identity.append(name.attrib["word"])
    Concept = " ".join(identity)

    # Check if we've found a concept
    if len(Concept) == 0:
        raise NoConceptException


    # TODO: Uitbreiden verkrijgen eigenschap
    relation = []
    properties = xml.xpath('//node[@pos="adj" and @rel="mod"] | //node[@rel="hd" and @pos="noun"] | //node[@rel="vc"]/node[@rel="hd"]')
    vraagwoorden = xml.xpath('//node[(@rel="whd" and (@root="wanneer" or @root="waar")) or (@rel="det" and @root="hoeveel")]')
    for prop in properties:
        relation.append(prop.attrib["word"])
    for vraagwoord in vraagwoorden:
        word = (vraagwoord.attrib["word"]).lower()
        if word == "wanneer" or word == "waar" or word == "hoeveel":
            relation = [word] + relation
    Property = " ".join(relation)

    # Check if we've found a property
    if len(Property) == 0:
        raise NoPropertyException

    return Concept, Property