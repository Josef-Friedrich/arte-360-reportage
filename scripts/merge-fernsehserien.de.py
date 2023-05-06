#! /usr/bin/env python

import typing
from lxml import etree


def get_text(element: typing.Any, tag: str):
    elements = element.xpath(tag)
    if len(elements) != 1:
        print(element)
        raise Exception("not found")
    return elements[0].text.strip()


def parseXML(xmlFile: str):
    """
    Parse the xml
    """
    with open(xmlFile) as fobj:
        xml = fobj.read()

    root = etree.fromstring(xml)

    for episode in root:
        print(get_text(episode, "date"))
        print(get_text(episode, "title"))
        print(get_text(episode, "url"))


if __name__ == "__main__":
    parseXML("fernsehserien.de.xml")
